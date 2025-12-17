using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;


public class UserInfoUpdateUI : MonoBehaviour
{
    [Header("Input Fields")]
    public TMP_InputField idInput;          // 본인 확인용 ID [cite: 29]
    public TMP_InputField currentPwInput;   // 본인 확인용 현재 비밀번호 [cite: 29]
    public TMP_InputField newPwInput;       // 변경할 새 비밀번호 [cite: 27]

    [Header("Profile Selection")]
    public int selectedProfileIndex = 0;    // 선택된 프로필 이미지 인덱스
    public Image[] profileSelectionHighlights; // 선택 표시용 이미지 배열

    [Header("Status Text")]
    public TextMeshProUGUI statusText;      // 결과 메시지 표시용

    void Start()
    {
    }

    private void OnEnable()
    {
        if (NetworkManager.Instance != null)
        {
            // 중복 방지를 위해 먼저 해제 후 다시 등록
            NetworkManager.Instance.OnUpdateUserInfoResult -= HandleUpdateResult;
            NetworkManager.Instance.OnUpdateUserInfoResult += HandleUpdateResult;
        }
    }

    private void OnDisable()
    {
        if (NetworkManager.Instance != null)
        {
            NetworkManager.Instance.OnUpdateUserInfoResult -= HandleUpdateResult;
        }
    }

    // 프로필 버튼 클릭 시 호출 (0~4 인덱스 설정)
    public void SetProfileIndex(int index)
    {
        selectedProfileIndex = index;

        // 선택 시각화 (테두리 활성화 등)
        for (int i = 0; i < profileSelectionHighlights.Length; i++)
        {
            if (profileSelectionHighlights[i] != null)
                profileSelectionHighlights[i].enabled = (i == index);
        }
    }

    // "정보 수정 완료" 버튼 클릭 시 호출
    public void OnClickUpdateSubmit()
    {
        string id = idInput.text;
        string currentPw = currentPwInput.text;
        string newPw = newPwInput.text;

        // 필수 입력 값 체크
        if (string.IsNullOrEmpty(id) || string.IsNullOrEmpty(currentPw) || string.IsNullOrEmpty(newPw))
        {
            statusText.text = "모든 정보를 입력해주세요.";
            return;
        }

        statusText.text = "서버에 정보 수정 요청 중...";

        // 서버로 업데이트 요청 전송 (ID, 현재PW, 새PW, 프로필인덱스) [cite: 32, 37]
        NetworkManager.Instance.SendUpdateUserInfo(id, currentPw, newPw, selectedProfileIndex);
    }

    // 서버 응답 처리 핸들러
    private void HandleUpdateResult(bool isSuccess)
    {
        if (isSuccess)
        {
            statusText.text = "<color=green>정보 수정 성공! 다시 로그인하세요.</color>";
            // 성공 시 입력 필드 초기화
            currentPwInput.text = "";
            newPwInput.text = "";
        }
        else
        {
            statusText.text = "<color=red>정보 수정 실패 (ID 혹은 현재 비밀번호 불일치).</color>";
        }
    }

    // UI 닫기 버튼 클릭 시
    public void OnClickClose()
    {
        gameObject.SetActive(false);
    }
}
