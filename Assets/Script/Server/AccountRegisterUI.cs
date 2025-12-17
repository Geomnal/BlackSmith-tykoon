using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class AccountRegisterUI : MonoBehaviour
{
    [Header("Input Fields")]
    public TMP_InputField idInput;
    public TMP_InputField pwInput;

    [Header("Profile Selection")]
    public int currentSelectedIndex = 0; // 선택된 인덱스 (0~4)
    public Image[] profileSelectionHighlights; // 선택 표시용 테두리나 이미지 (옵션)

    // 프로필 버튼 클릭 시 호출 (Unity 인스펙터에서 0, 1, 2, 3, 4로 각각 할당)
    public void SetProfileIndex(int index)
    {
        currentSelectedIndex = index;

        // 시각적 강조 피드백
        for (int i = 0; i < profileSelectionHighlights.Length; i++)
        {
            profileSelectionHighlights[i].enabled = (i == index);
        }

        Debug.Log($"프로필 {index}번 선택됨");
    }

    // "회원가입 완료" 버튼 클릭 시 호출
    public void OnClickSubmitRegistration()
    {
        string id = idInput.text;
        string pw = pwInput.text;

        if (string.IsNullOrEmpty(id) || string.IsNullOrEmpty(pw))
        {
            Debug.LogWarning("아이디와 비밀번호를 모두 입력하세요.");
            return;
        }

        // NetworkManager를 통해 서버로 데이터 전송
        NetworkManager.Instance.SendCreateAccount(id, pw, currentSelectedIndex);

        Debug.Log($"회원가입 요청 전송 - ID: {id}, ProfileIndex: {currentSelectedIndex}");
    }
}
