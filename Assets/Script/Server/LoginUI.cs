using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class LoginUI : MonoBehaviour
{
    [Header("UI 컴포넌트 연결")]
    public TMP_InputField idInput;       // 아이디 입력창
    public TMP_InputField pwInput;       // 비밀번호 입력창
    public Button loginButton;           // 로그인 버튼
    public Button registerButton;        // 회원가입 버튼
    public TextMeshProUGUI statusText;   // 상태 메시지 (ex: "로그인 성공!")
    public ProfileSelector profileSelector;

    public Button changePwButton;  // 비밀번호 변경 버튼 연결
    public Button deleteAccButton; // 계정 탈퇴 버튼 연결

    public GameObject InfoObject;

    void Start()
    {
        // 버튼에 함수 연결
        loginButton.onClick.AddListener(OnClickLogin);
        registerButton.onClick.AddListener(OnClickRegister);

        // NetworkManager 이벤트 구독 (서버 응답 오면 실행될 함수들)
        NetworkManager.Instance.OnLoginResult += HandleLoginResult;
        NetworkManager.Instance.OnCreateAccountResult += HandleRegisterResult;

        changePwButton.onClick.AddListener(OnClickChangeInfoButton);
        deleteAccButton.onClick.AddListener(OnClickDeleteAccount);

        // 결과 이벤트 구독
        NetworkManager.Instance.OnChangePasswordResult += HandleChangePasswordResult;
        NetworkManager.Instance.OnDeleteAccountResult += HandleDeleteAccountResult;
    }

    void OnDestroy()
    {
        // 이벤트 구독 해제 (중복 방지)
        if (NetworkManager.Instance != null)
        {
            NetworkManager.Instance.OnLoginResult -= HandleLoginResult;
            NetworkManager.Instance.OnCreateAccountResult -= HandleRegisterResult;
        }
    }

    // --- [버튼 클릭 시 실행] ---

    void OnClickLogin()
    {
        string id = idInput.text;
        string pw = pwInput.text;

        if (string.IsNullOrEmpty(id) || string.IsNullOrEmpty(pw))
        {
            statusText.text = "아이디와 비밀번호를 입력하세요.";
            return;
        }

        statusText.text = "로그인 시도 중...";
        NetworkManager.Instance.SendLogin(id, pw);
    }

    void OnClickRegister()
    {
        string id = idInput.text;
        string pw = pwInput.text;
        int profileIdx = profileSelector.SelectedIndex; // 선택된 값 가져오기

        if (string.IsNullOrEmpty(id) || string.IsNullOrEmpty(pw))
        {
            statusText.text = "정보를 입력하세요.";
            return;
        }

        NetworkManager.Instance.SendCreateAccount(id, pw, profileIdx); // 인덱스 추가 전
    }
    // [비밀번호 변경 요청]
    void OnClickChangePassword()
    {
        string id = idInput.text;        // 유저 ID
        string currentPw = pwInput.text; // 현재 비밀번호 (화면상 가독성을 위해 PW필드 활용)
                                         // 실제 구현 시에는 "ID/현재PW/새PW"를 넣기 위해 입력을 더 받거나 순차적으로 처리 가능
                                         // 여기서는 간단히 PW필드에 "현재비번,새비번" 콤마로 구분해서 받는다고 가정하거나 전용 인풋을 하나 더 추천합니다.

        statusText.text = "비밀번호 변경 시도 중...";
        // 예시: idInput은 ID, pwInput은 "현재PW:새PW" 형식으로 입력받을 때
        string[] pws = pwInput.text.Split(':');
        if (pws.Length < 2)
        {
            statusText.text = "PW필드에 '현재비번:새비번' 형식으로 입력하세요.";
            return;
        }
        NetworkManager.Instance.SendChangePassword(id, pws[0], pws[1]);
    }

    void OnClickChangeInfoButton()
    {
        InfoObject.SetActive(true);
    }

    // [계정 탈퇴 요청]
    void OnClickDeleteAccount()
    {
        string id = idInput.text;
        string pw = pwInput.text;

        if (string.IsNullOrEmpty(id) || string.IsNullOrEmpty(pw))
        {
            statusText.text = "탈퇴를 위해 ID와 PW를 모두 입력하세요.";
            return;
        }

        statusText.text = "계정 탈퇴 시도 중...";
        NetworkManager.Instance.SendDeleteAccount(id, pw);
    }

    // --- [결과 처리 핸들러] ---
    void HandleChangePasswordResult(bool isSuccess)
    {
        statusText.text = isSuccess ? "비밀번호 변경 성공!" : "비밀번호 변경 실패 (정보 불일치).";
    }

    void HandleDeleteAccountResult(bool isSuccess)
    {
        statusText.text = isSuccess ? "계정이 성공적으로 삭제되었습니다." : "계정 삭제 실패 (정보 불일치).";
    }

    // --- [서버 응답 처리] ---

    void HandleLoginResult(bool isSuccess)
    {
        if (isSuccess)
        {
            statusText.text = "로그인 성공! 게임 진입...";
            // 로그인 성공 시 게임 씬으로 이동 (씬 이름 확인 필요)
            SceneManager.LoadScene("main");
        }
        else
        {
            statusText.text = "로그인 실패. 아이디/비번을 확인하세요.";
        }
    }

    void HandleRegisterResult(bool isSuccess)
    {
        if (isSuccess)
        {
            statusText.text = "회원가입 성공! 이제 로그인하세요.";
        }
        else
        {
            statusText.text = "회원가입 실패 (이미 존재하는 ID입니다).";
        }
    }
}
