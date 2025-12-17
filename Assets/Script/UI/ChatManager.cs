using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using System;

public class ChatManager : MonoBehaviour
{
    public TMP_InputField chatInputField; // 입력창
    public Transform chatContent;         // ScrollView의 Content (프리팹이 생성될 부모)
    public GameObject chatItemPrefab;     // 채팅 바 프리팹

    void Start()
    {
        // 서버로부터 채팅 알림을 받았을 때 실행될 이벤트 구독
        NetworkManager.Instance.OnChatReceived += AddChatLog;
    }

    // 전송 버튼 클릭 시 호출
    public void OnClickSend()
    {
        if (string.IsNullOrEmpty(chatInputField.text)) return;

        // 서버로 채팅 요청 전송
        NetworkManager.Instance.SendChat(chatInputField.text);
        chatInputField.text = ""; // 입력창 초기화
    }

    // 서버 알림 패킷 수신 시 호출 (UnityMainThreadDispatcher 활용 필수)
    public void AddChatLog(string userId, string message, int profileIndex)
    {
        // 메인 스레드에서 UI 생성
        UnityMainThreadDispatcher.Instance.Enqueue(() =>
        {
            GameObject newChat = Instantiate(chatItemPrefab, chatContent);
            ChatItem item = newChat.GetComponent<ChatItem>();

            // 데이터 설정
            item.SetChat(userId, message, profileIndex);

            // 스크롤을 최하단으로 내리는 로직을 여기에 추가할 수 있습니다.
        });
    }
}
