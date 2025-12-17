using System.Collections;
using System.Collections.Generic;
using CSBaseLib;
using UnityEngine;

public class RankingManager : MonoBehaviour
{
    [Header("UI Reference")]
    public GameObject rankingItemPrefab; // 랭킹 한 줄을 나타내는 프리팹
    public Transform rankingContent;    // ScrollView의 Content 오브젝트

    private void Start()
    {
        // 1. 서버로부터 랭킹 데이터를 받았을 때 실행될 이벤트 구독
        if (NetworkManager.Instance != null)
        {
            NetworkManager.Instance.OnRankingReceived += UpdateRankingUI;
        }

        // 2. 창이 열릴 때 서버에 최신 랭킹 요청
        RequestRanking();
    }
    private void OnEnable()
    {
        if (NetworkManager.Instance != null)
        {
            // 이벤트 구독
            NetworkManager.Instance.OnRankingReceived += UpdateRankingUI;
            // 랭킹 데이터 요청
            NetworkManager.Instance.RequestRanking();
        }
    }

    private void OnDisable()
    {
        if (NetworkManager.Instance != null)
        {
            // 이벤트 구독 해제 (메모리 누수 방지)
            NetworkManager.Instance.OnRankingReceived -= UpdateRankingUI;
        }
    }

    public void RequestRanking()
    {
        Debug.Log("서버에 랭킹 리스트 요청 중...");
        NetworkManager.Instance.RequestRanking();
    }

    // 서버 응답 수신 시 호출되는 함수
    public void UpdateRankingUI(List<RankingData> rankList)
    {
        UnityMainThreadDispatcher.Instance.Enqueue(() =>
        {
            foreach (Transform child in rankingContent)
            {
                Destroy(child.gameObject);
            }

            foreach (var data in rankList)
            {
                GameObject newItem = Instantiate(rankingItemPrefab, rankingContent);
                RankingItem itemScript = newItem.GetComponent<RankingItem>();

                if (itemScript != null)
                {
                    // 서버에서 결합해준 ProfileIndex를 넘겨줌
                    itemScript.SetInfo(data.Rank, data.UserID, data.Score, data.ProfileIndex);
                }
            }
        });
    }

    private void OnDestroy()
    {
        // 이벤트 구독 해제
        if (NetworkManager.Instance != null)
        {
            NetworkManager.Instance.OnRankingReceived -= UpdateRankingUI;
        }
    }
}
