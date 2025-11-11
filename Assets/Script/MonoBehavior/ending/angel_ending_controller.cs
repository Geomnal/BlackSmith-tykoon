using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

public class angel_ending_controller : MonoBehaviour
{
    private PlayerManager playerManager;

    [SerializeField] private GameObject endingprefab;

    [SerializeField] private TextMeshProUGUI angeltext;
    [SerializeField] private TextMeshProUGUI leveltext;

    
    // Start is called before the first frame update
    void Start()
    {
        playerManager = PlayerManager.instance;
        angeltext.text = $"보유 선 수치 :{playerManager.morality } ";
        leveltext.text = $"플레이어 레벨 :{playerManager.Playerlevel} ";
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void go_ending_button_click()
    {

        if (playerManager.Playerlevel >= 5 && playerManager.morality >= 99)
        {
            SceneManager.LoadScene("AngelEnding");
        }
    }
    public void DestroyPrefab()
    {
        if (endingprefab != null)
        {
            Destroy(endingprefab); // endingPrefab을 삭제
            Debug.Log("endingPrefab이 삭제되었습니다.");
        }
        else
        {
            Debug.LogWarning("endingPrefab이 할당되지 않았습니다.");
        }
    }
}
