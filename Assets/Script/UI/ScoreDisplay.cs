using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class ScoreDisplay : MonoBehaviour
{
    public TMP_Text scoreText;
    private bool isRequestingScore = false;

    void Start()
    {
        // 1. 서버 응답 이벤트에 UI 업데이트 함수를 등록합니다.
        NetworkManager.Instance.OnScoreReceived += UpdateScoreUI;

        // 2. 게임 시작 시 서버에 점수를 요청합니다.
        RequestServerScore();
    }

    void RequestServerScore()
    {
        if (isRequestingScore) return;

        // 실제 유저 ID를 사용하세요. (현재는 "Test"로 가정)
        NetworkManager.Instance.RequestUserScore("Test");
        isRequestingScore = true;
    }

    // 서버 응답이 메인 스레드로 전달되면 이 함수가 호출됩니다.
    public void UpdateScoreUI(int newScore)
    {
        if (scoreText != null)
        {
            scoreText.text = $"Score: {newScore}"; // 서버에서 받은 실제 점수 반영
            isRequestingScore = false;
        }
    }

    void OnDestroy()
    {
        if (NetworkManager.Instance != null)
        {
            NetworkManager.Instance.OnScoreReceived -= UpdateScoreUI;
        }
    }
}
