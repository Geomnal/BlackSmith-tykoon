using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

public class evil_ending_controller : MonoBehaviour
{
    private PlayerManager playerManager;

    [SerializeField] private GameObject endingprefab;

    private int evil_morality = 0;

    [SerializeField] private TextMeshProUGUI eviltext;
    [SerializeField] private TextMeshProUGUI leveltext;
    // Start is called before the first frame update
    void Start()
    {
        playerManager = PlayerManager.instance;
        evil_morality = 100 - playerManager.morality;
        eviltext.text = $"보유 악 수치 :{evil_morality} ";
        leveltext.text = $"플레이어 레벨 :{playerManager.Playerlevel} ";
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void go_ending_button_click()
    {
        evil_morality = 100 - playerManager.morality;
        if (playerManager.Playerlevel >= 5 && evil_morality >= 99)
        {
            SceneManager.LoadScene("EvilEnding");
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
