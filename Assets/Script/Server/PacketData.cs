using MessagePack; //https://github.com/neuecc/MessagePack-CSharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSBaseLib
{
    public struct PacketData
    {
        public Int16 DataSize;
        public Int16 PacketID;
        public SByte Type;
        public byte[] BodyData;
    }
    public class PacketDef
    {
        public const Int16 HeaderSize = 5;
        public const int MAX_USER_ID_BYTE_LENGTH = 16;
        public const int MAX_USER_PW_BYTE_LENGTH = 16;

        public const int INVALID_ROOM_NUMBER = -1;
    }

    public class PacketToBytes
    {
        public static byte[] Make(PacketId packetID, byte[] bodyData)
        {
            byte type = 0;
            var pktID = (UInt16)packetID;
            UInt16 bodyDataSize = 0;
            if (bodyData != null)
            {
                bodyDataSize = (UInt16)bodyData.Length;
            }
            var packetSize = (UInt16)(bodyDataSize + PacketDef.HeaderSize);
                        
            var dataSource = new byte[packetSize];
            Buffer.BlockCopy(BitConverter.GetBytes(packetSize), 0, dataSource, 0, 2);
            Buffer.BlockCopy(BitConverter.GetBytes(pktID), 0, dataSource, 2, 2);
            dataSource[4] = type;
            
            if (bodyData != null)
            {
                Buffer.BlockCopy(bodyData, 0, dataSource, 5, bodyDataSize);
            }

            return dataSource;
        }

        public static Tuple<int, byte[]> ClientReceiveData(int recvLength, byte[] recvData)
        {
            var packetSize = BitConverter.ToUInt16(recvData, 0);
            var packetID = BitConverter.ToUInt16(recvData, 2);
            var bodySize = packetSize - PacketDef.HeaderSize;

            var packetBody = new byte[bodySize];
            Buffer.BlockCopy(recvData, PacketDef.HeaderSize, packetBody,  0, bodySize);

            return new Tuple<int, byte[]>(packetID, packetBody);
        }
    }

    [MessagePackObject]
    public class PKReqLogin
    {
        [Key(0)] public string UserID;
        [Key(1)] public string AuthToken;
    }

    [MessagePackObject]
    public class PKResLogin
    {
        [Key(0)] public short Result; // ErrorCode
        [Key(1)] public string UserID;
        [Key(2)] public int CurrentScore;
    }

    // --- [점수 추가] ---
    [MessagePackObject]
    public class PKTReqUserScoreAdd
    {
        [Key(0)] public string UserID;
        [Key(1)] public int AddScore;
    }

    [MessagePackObject]
    public class PKTResUserScoreAdd
    {
        [Key(0)] public short Result;
        [Key(1)] public int FinalScore;
    }

    // --- [랭킹] ---
    [MessagePackObject]
    public class PKTReqUserRankingList
    {
        [Key(0)] public string UserID;
    }

    [MessagePackObject]
    public class PKTResUserRankingList
    {
        [Key(0)] public List<RankingData> RankList;
    }

    [MessagePackObject]
    public class RankingData
    {
        [Key(0)] public string UserID;
        [Key(1)] public int Score;
        [Key(2)] public int Rank;
        [Key(3)] public int ProfileIndex;
    }

    // --- [채팅] ---
    [MessagePackObject]
    public class PKTReqRoomChat
    {
        [Key(0)] public string ChatMessage;
    }

    [MessagePackObject]
    public class PKTNtfRoomChat
    {
        [Key(0)] public string UserID;
        [Key(1)] public string ChatMessage;
        [Key(2)]
        public int ProfileIndex;
    }
    [MessagePackObject] public class PKTReqUserScoreGet { [Key(0)] public string UserID; }
    [MessagePackObject] public class PKTResUserScoreGet { [Key(0)] public short Result; [Key(1)] public int Score; }

    [MessagePackObject]
    public class PKReqCreateAccount
    {
        [Key(0)] public string UserID;
        [Key(1)] public string Password; // AuthToken 대신 Password 사용
        [Key(2)]
        public int ProfileIndex;
    }

    // [추가] 회원가입 응답
    [MessagePackObject]
    public class PKResCreateAccount
    {
        [Key(0)] public short Result; // ErrorCode
    }
    [MessagePackObject]
    public class PKTReqChangePassword
    {
        [Key(0)] public string UserID;
        [Key(1)] public string CurrentPassword;
        [Key(2)] public string NewPassword;
    }

    [MessagePackObject]
    public class PKTResChangePassword
    {
        [Key(0)] public short Result; // ErrorCode
    }

    [MessagePackObject]
    public class PKTReqDeleteAccount
    {
        [Key(0)] public string UserID;
        [Key(1)] public string Password;
    }

    [MessagePackObject]
    public class PKTResDeleteAccount
    {
        [Key(0)] public short Result;
    }

    [MessagePackObject]
    public class PKTReqUpdateUserInfo
    {
        [Key(0)] public string UserID;          // 대상 ID 
        [Key(1)] public string CurrentPassword; // 본인 확인을 위한 현재 비밀번호 [cite: 29, 37]
        [Key(2)] public string NewPassword;     // 변경할 새 비밀번호 
        [Key(3)] public int ProfileIndex;       // 변경할 프로필 사진 인덱스 [cite: 36]
    }

    [MessagePackObject]
    public class PKTResUpdateUserInfo
    {
        [Key(0)] public short Result; // ErrorCode.NONE(0) 이면 성공 [cite: 29]
    }
}
