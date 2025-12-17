using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using ChatClient2;
using CSBaseLib;
using MessagePack;
#if UNITY_EDITOR
using UnityEditor;
using UnityEditor.PackageManager;
#endif
using UnityEngine;
using UnityEngine.SocialPlatforms.Impl;

// 서버와 통신을 담당하는 핵심 매니저 클래스
public sealed class NetworkManager
{
    // 싱글톤 패턴 구현
    private static readonly Lazy<NetworkManager> _instance = new(() => new NetworkManager());
    public static NetworkManager Instance => _instance.Value;

    private bool _isInitialized = false;

    // TCP 통신 래퍼 클래스
    ClientSimpleTcp Network = new ClientSimpleTcp();

    // 스레드 제어 플래그
    bool IsNetworkThreadRunning = false;
    bool IsBackGroundProcessRunning = false;
    /// <summary>
    /// [UI 연동을 위한 이벤트 (Action)]
    /// UI 스크립트에서 이 이벤트들을 구독(Subscribe)하여 화면을 갱신합니다.
    /// </summary>
    public Action<bool> OnLoginResult;                 // 로그인 성공/실패 알림
    public Action<string, string, int> OnChatReceived;
    public Action<List<RankingData>> OnRankingReceived; // 랭킹 리스트 수신
    public Action<int> OnScoreReceived;                // 점수 획득 결과 알림 (현재 점수)
    public Action<bool> OnCreateAccountResult;
    public Action<bool> OnChangePasswordResult; // 비밀번호 변경 결과
    public Action<bool> OnDeleteAccountResult;   // 계정 탈퇴 결과
    public Action<bool> OnUpdateUserInfoResult;// 유저 정보 업데이트 결과


    // 스레드 정의
    System.Threading.Thread NetworkReadThread = null;
    System.Threading.Thread NetworkSendThread = null;
    System.Threading.Thread BackGroundProcessThread = null;

    // 패킷 버퍼 및 큐
    PacketBufferManager PacketBuffer = new PacketBufferManager();
    Queue<PacketData> RecvPacketQueue = new Queue<PacketData>();
    Queue<byte[]> SendPacketQueue = new Queue<byte[]>();


    private NetworkManager() { }

    // 초기화 및 서버 연결
    public void Initialize()
    {
        if (_isInitialized) return;

        // 패킷 버퍼 초기화
        PacketBuffer.Init((8096 * 10), PacketDef.HeaderSize, 1024);

        // 스레드 시작
        IsNetworkThreadRunning = true;
        NetworkReadThread = new System.Threading.Thread(this.NetworkReadProcess);
        NetworkReadThread.Start();
        NetworkSendThread = new System.Threading.Thread(this.NetworkSendProcess);
        NetworkSendThread.Start();

        IsBackGroundProcessRunning = true;
        BackGroundProcessThread = new System.Threading.Thread(this.BackGroundProcess);
        BackGroundProcessThread.Start();

        // 서버 연결 시도 (IP와 Port는 서버 설정에 맞게 변경)
        bool bNetwork = Network.Connect("127.0.0.1", 32452);

        if (bNetwork)
        {
            Debug.Log("서버에 접속 성공 !!!");
        }
        else
        {
            Debug.LogError("서버에 접속 실패 !!!");
        }

        _isInitialized = true;
    }

    // 서버 연결 종료
    public void Stop()
    {
        IsNetworkThreadRunning = false;
        IsBackGroundProcessRunning = false;
        Network.Close();
    }

    // =================================================================
    // [패킷 전송 함수 (Client -> Server)]
    // UI나 게임 로직에서 호출하는 함수들입니다.
    // =================================================================

    // 1. 로그인 요청
    public void SendLogin(string userId, string authToken)
    {
        var request = new PKReqLogin { UserID = userId, AuthToken = authToken };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_LOGIN, body);
        PostSendPacket(sendData);
    }

    // 2. 채팅 메시지 전송
    public void SendChat(string message)
    {
        var request = new PKTReqRoomChat { ChatMessage = message };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_ROOM_CHAT, body);
        PostSendPacket(sendData);
    }

    // 3. 랭킹 리스트 요청
    public void RequestRanking()
    {
        // 소켓 연결 상태 확인 (NullReference 방지)
        if (Network == null || Network.IsConnected() == false)
        {
            Debug.LogWarning("서버에 연결되지 않아 랭킹을 요청할 수 없습니다.");
            return;
        }

        if (PlayerManager.instance == null)
        {
            Debug.LogError("PlayerManager 인스턴스가 존재하지 않습니다.");
            return;
        }

        var request = new PKTReqUserRankingList { UserID = PlayerManager.instance.UserID };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_USER_RANKING_LIST, body);
        PostSendPacket(sendData);
    }

    // 4. 점수 획득 (무기 제작 성공 시 호출)
    public void SendScoreAdd(int scoreIncrease)
    {
        var request = new PKTReqUserScoreAdd { AddScore = scoreIncrease };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_USER_SCORE_ADD, body);
        PostSendPacket(sendData);
    }

    // 패킷 큐에 데이터 등록
    public void PostSendPacket(byte[] sendData)
    {
        if (Network.IsConnected() == false)
        {
            Debug.LogWarning("서버 연결이 되어 있지 않습니다");
            return;
        }
        lock (((System.Collections.ICollection)SendPacketQueue).SyncRoot)
        {
            SendPacketQueue.Enqueue(sendData);
        }
    }

    // =================================================================
    // [패킷 수신 처리 (Server -> Client)]
    // 백그라운드 스레드에서 패킷을 꺼내 처리합니다.
    // =================================================================
    void BackGroundProcess()
    {
        while (IsBackGroundProcessRunning)
        {
            try
            {
                var packet = new PacketData();
                lock (((System.Collections.ICollection)RecvPacketQueue).SyncRoot)
                {
                    if (RecvPacketQueue.Count() > 0)
                    {
                        packet = RecvPacketQueue.Dequeue();
                    }
                    else
                    {
                        // 큐가 비었으면 잠시 대기
                        Thread.Sleep(1);
                        continue;
                    }
                }

                if (packet.PacketID != 0)
                {
                    PacketProcess(packet);
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"Packet Process Error: {ex.Message}");
            }
        }
    }

    // 실제 패킷 로직 처리 (Switch문)
    void PacketProcess(PacketData packet)
    {
        switch ((PacketId)packet.PacketID)
        {
            // 1. 로그인 응답 처리
            case PacketId.RES_LOGIN:
                {
                    var resData = MessagePackSerializer.Deserialize<PKResLogin>(packet.BodyData);
                    Debug.Log($"[Login] Result: {resData.Result}, ID: {resData.UserID}");

                    // 메인 스레드(UI)로 이벤트 전달
                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            bool isSuccess = (resData.Result == (short)CSBaseLib.ErrorCode.NONE);
                            OnLoginResult?.Invoke(isSuccess);
                        });
                    }
                }
                break;

            // 2. 채팅 수신 (브로드캐스트)
            case PacketId.NTF_ROOM_CHAT:
                {
                    var ntfData = MessagePackSerializer.Deserialize<PKTNtfRoomChat>(packet.BodyData);

                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            // ntfData에서 ProfileIndex도 함께 꺼내서 Invoke 합니다.
                            OnChatReceived?.Invoke(ntfData.UserID, ntfData.ChatMessage, ntfData.ProfileIndex);
                        });
                    }
                }
                break;

            // 3. 랭킹 리스트 수신
            case PacketId.RES_USER_RANKING_LIST:
                {
                    var resData = MessagePackSerializer.Deserialize<PKTResUserRankingList>(packet.BodyData);

                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            OnRankingReceived?.Invoke(resData.RankList);
                        });
                    }
                }
                break;

            // 4. 점수 획득 결과 수신
            case PacketId.RES_USER_SCORE_ADD:
                {
                    var resData = MessagePackSerializer.Deserialize<PKTResUserScoreAdd>(packet.BodyData);
                    Debug.Log($"[Score] Final Score: {resData.FinalScore}");

                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            OnScoreReceived?.Invoke(resData.FinalScore);
                        });
                    }
                }
                break;
            case PacketId.RES_CREATE_ACCOUNT:
                {
                    var resData = MessagePackSerializer.Deserialize<PKResCreateAccount>(packet.BodyData);

                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            bool isSuccess = (resData.Result == (short)CSBaseLib.ErrorCode.NONE);
                            if (isSuccess) Debug.Log("회원가입 성공!");
                            else Debug.Log("회원가입 실패: 중복된 ID입니다.");

                            // UI에 결과 알림
                            OnCreateAccountResult?.Invoke(isSuccess);
                        });
                    }
                }
                break;
            case PacketId.RES_CHANGE_PASSWORD:
                {
                    var resData = MessagePackSerializer.Deserialize<PKTResChangePassword>(packet.BodyData);
                    UnityMainThreadDispatcher.Instance.Enqueue(() => {
                        bool isSuccess = (resData.Result == (short)CSBaseLib.ErrorCode.NONE);
                        OnChangePasswordResult?.Invoke(isSuccess);
                    });
                }
                break;

            case PacketId.RES_DELETE_ACCOUNT:
                {
                    var resData = MessagePackSerializer.Deserialize<PKTResDeleteAccount>(packet.BodyData);
                    UnityMainThreadDispatcher.Instance.Enqueue(() => {
                        bool isSuccess = (resData.Result == (short)CSBaseLib.ErrorCode.NONE);
                        OnDeleteAccountResult?.Invoke(isSuccess);
                    });
                }
                break;
            case PacketId.RES_USER_INFO_UPDATE:
                {
                    // 1. 서버에서 보낸 응답 데이터를 역직렬화합니다.
                    var resData = MessagePackSerializer.Deserialize<PKTResUpdateUserInfo>(packet.BodyData);

                    // 2. 유니티 메인 스레드에서 UI를 갱신할 수 있도록 Enqueue 합니다.
                    UnityMainThreadDispatcher.Instance.Enqueue(() =>
                    {
                        bool isSuccess = (resData.Result == (short)CSBaseLib.ErrorCode.NONE);

                        // 3. UserInfoUpdateUI가 구독 중인 이벤트를 호출합니다.
                        OnUpdateUserInfoResult?.Invoke(isSuccess);

                        Debug.Log($"정보 수정 결과 수신: {isSuccess}");
                    });
                }
                break;

        }
    }

    public void SendCreateAccount(string userId, string password, int profileIndex)
    {
        var request = new PKReqCreateAccount
        {
            UserID = userId,
            Password = password,
            ProfileIndex = profileIndex // 패킷 데이터에 포함
        };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_CREATE_ACCOUNT, body);
        PostSendPacket(sendData);
    }
    public void SendUpdateUserInfo(string userId, string currentPw, string newPw, int profileIdx)
    {
        var request = new PKTReqUpdateUserInfo
        {
            UserID = userId,
            CurrentPassword = currentPw,
            NewPassword = newPw,
            ProfileIndex = profileIdx
        };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_USER_INFO_UPDATE, body);
        PostSendPacket(sendData);
}
    public void SendChangePassword(string userId, string currentPw, string newPw)
    {
        var request = new PKTReqChangePassword
        {
            UserID = userId,
            CurrentPassword = currentPw,
            NewPassword = newPw
        };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_CHANGE_PASSWORD, body);
        PostSendPacket(sendData);
    }

    // [서버로 전송] 계정 탈퇴 요청
    public void SendDeleteAccount(string userId, string password)
    {
        var request = new PKTReqDeleteAccount
        {
            UserID = userId,
            Password = password
        };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_DELETE_ACCOUNT, body);
        PostSendPacket(sendData);
    }

    void NetworkReadProcess()
    {
        while (IsNetworkThreadRunning)
        {
            if (Network.IsConnected() == false)
            {
                Thread.Sleep(10);
                continue;
            }

            var recvData = Network.Receive();

            if (recvData != null)
            {
                // 버퍼에 데이터 쓰기
                PacketBuffer.Write(recvData.Item2, 0, recvData.Item1);

                while (true)
                {
                    // 버퍼에서 패킷 완성본 읽기
                    var data = PacketBuffer.Read();
                    if (data.Count < 1) break;

                    var packet = new PacketData();
                    packet.DataSize = (short)(data.Count - PacketDef.HeaderSize);
                    packet.PacketID = BitConverter.ToInt16(data.Array, data.Offset + 2);
                    packet.Type = (SByte)data.Array[(data.Offset + 4)];
                    packet.BodyData = new byte[packet.DataSize];
                    Buffer.BlockCopy(data.Array, (data.Offset + PacketDef.HeaderSize), packet.BodyData, 0, packet.DataSize);

                    lock (((System.Collections.ICollection)RecvPacketQueue).SyncRoot)
                    {
                        RecvPacketQueue.Enqueue(packet);
                    }
                }
            }
            else
            {
                // 수신 데이터가 null이면 연결 끊김으로 간주
                // 필요 시 재연결 로직 추가 가능
            }
        }
    }

    void NetworkSendProcess()
    {
        while (IsNetworkThreadRunning)
        {
            if (Network.IsConnected() == false)
            {
                Thread.Sleep(10);
                continue;
            }

            lock (((System.Collections.ICollection)SendPacketQueue).SyncRoot)
            {
                if (SendPacketQueue.Count > 0)
                {
                    var packet = SendPacketQueue.Dequeue();
                    Network.Send(packet);
                }
            }
            Thread.Sleep(1);
        }
    }

    public void RequestUserScore(string userId)
    {
        var request = new PKTReqUserScoreGet { UserID = userId };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_USER_SCORE_GET, body);
        PostSendPacket(sendData);
    }
}