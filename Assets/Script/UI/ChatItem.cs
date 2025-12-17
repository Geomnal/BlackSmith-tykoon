using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class ChatItem : MonoBehaviour
{
    public Image profileImage;      // 프로필 아이콘 이미지
    public TextMeshProUGUI nameText; // 유저 이름 텍스트
    public TextMeshProUGUI msgText;  // 채팅 내용 텍스트

    public Sprite[] profileSprites; // 미리 등록해둔 프로필 스프라이트 배열 (0~4)

    public void SetChat(string name, string message, int profileIndex)
    {
        nameText.text = name;
        msgText.text = message;

        // 인덱스 범위 체크 후 이미지 교체
        if (profileIndex >= 0 && profileIndex < profileSprites.Length)
        {
            profileImage.sprite = profileSprites[profileIndex];
        }
    }
}
