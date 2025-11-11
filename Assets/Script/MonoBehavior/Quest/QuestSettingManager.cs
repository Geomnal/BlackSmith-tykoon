using System.Collections;
using System.Collections.Generic;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;

public class QuestSettingManager : MonoBehaviour
{
    public static QuestSettingManager instance;
    private PlayerManager playerManager;
    [SerializeField]private List<GameObject> PlayerLevel1quest;
    [SerializeField]private List<GameObject> PlayerLevel2publicquest;
    [SerializeField]private List<GameObject> PlayerLevel2angelquest;
    [SerializeField]private List<GameObject> PlayerLevel2evilquest;
    [SerializeField]private List<GameObject> PlayerLevel3publicquest;
    [SerializeField]private List<GameObject> PlayerLevel3angelquest;
    [SerializeField]private List<GameObject> PlayerLevel3evilquest;
    [SerializeField]private List<GameObject> PlayerLevel4publicquest;
    [SerializeField]private List<GameObject> PlayerLevel4angelquest;
    [SerializeField]private List<GameObject> PlayerLevel4evilquest;
    [SerializeField]private List<GameObject> PlayerLevel5publicquest;
    [SerializeField]private List<GameObject> PlayerLevel5angelquest;
    [SerializeField] private List<GameObject> PlayerLevel5evilquest;
    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else
        {
            Destroy(gameObject); // 이미 인스턴스가 존재하면 새로 생긴 객체를 파괴

        }
    }
    // Start is called before the first frame update
    private void Start()
    {
        playerManager = PlayerManager.instance;
        Level1Quest();
    }

    // Update is called once per frame
    private void Update()
    {

    }
    private void Level1Quest()
    {
        foreach(GameObject questObject in PlayerLevel1quest)
        {
            questObject.SetActive(true);
        }
    }
    public void Level2publicQuest()
    {
        if(playerManager.Playerlevel >= 2)
        {
            foreach (GameObject questObject in PlayerLevel2publicquest)
            {
                questObject.SetActive(true);
            }
        }
    }
    public void Level3publicQuest()
    {
        if (playerManager.Playerlevel >= 3)
        {
            foreach (GameObject questObject in PlayerLevel3publicquest)
            {
                questObject.SetActive(true);
            }
        }
    }

    public void Level4publicQuest()
    {
        if (playerManager.Playerlevel >= 4)
        {
            foreach (GameObject questObject in PlayerLevel4publicquest)
            {
                questObject.SetActive(true);
            }
        }
    }

    public void Level5publicQuest()
    {
        
        if (playerManager.Playerlevel >= 5 && PlayerLevel5publicquest != null)
        {
            foreach (GameObject questObject in PlayerLevel5publicquest)
            {
                questObject.SetActive(true);
            }
        }
    }
    public void LevelUp_Quest_open()
    {
        Level2publicQuest();
        Level3publicQuest();
        Level4publicQuest();
        Level5publicQuest();
        moralty_up_Quest_open();
    }
    public void moralty_up_Quest_open()
    {
        if (playerManager.Playerlevel >= 2)
        {
            moralty_up_Quest_open_level2();
        }

        if (playerManager.Playerlevel >= 3)
        {
            moralty_up_Quest_open_level3();
        }

        if (playerManager.Playerlevel >= 4)
        {
            moralty_up_Quest_open_level4();
        }

        if (playerManager.Playerlevel >= 5)
        {
            moralty_up_Quest_open_level5();
        }
    }
    public void moralty_up_Quest_open_level2()
    {
        if (playerManager.morality >= 50 && playerManager.Playerlevel >= 2)
        {
            foreach (GameObject questObject in PlayerLevel2angelquest)
            {
                questObject.SetActive(true);
            }
            foreach (GameObject questObject in PlayerLevel2evilquest)
            {
                questObject.SetActive(false);
            }

        }
        else if(playerManager.morality <= 49 && playerManager.Playerlevel >= 2)
        {
            foreach (GameObject questObject in PlayerLevel2evilquest)
            {
                questObject.SetActive(true);
            }
            foreach (GameObject questObject in PlayerLevel2angelquest)
            {
                questObject.SetActive(false);
            }
        }

       
    }
    public void moralty_up_Quest_open_level3()
    {
        if (playerManager.morality >= 50)
        {
            foreach (GameObject questObject in PlayerLevel3angelquest)
            {
                questObject.SetActive(true);
            }
            foreach (GameObject questObject in PlayerLevel3evilquest)
            {
                questObject.SetActive(false);
            }
        }
        else
        {
            foreach (GameObject questObject in PlayerLevel3evilquest)
            {
                questObject.SetActive(true);
            }
            foreach (GameObject questObject in PlayerLevel3angelquest)
            {
                questObject.SetActive(false);
            }
        }
    }
    public void moralty_up_Quest_open_level4()
    {
        if (playerManager.morality >= 50)
        {
            foreach (GameObject questObject in PlayerLevel4angelquest)
            {
                questObject.SetActive(true);
            }
            foreach (GameObject questObject in PlayerLevel4evilquest)
            {
                questObject.SetActive(false);
            }
        }
        else
        {
            foreach (GameObject questObject in PlayerLevel4evilquest)
            {
                questObject.SetActive(true);
            }
            foreach (GameObject questObject in PlayerLevel4angelquest)
            {
                questObject.SetActive(false);
            }
        }
    }

    public void moralty_up_Quest_open_level5()
    {
        if (playerManager.morality >= 50)
        {
            foreach (GameObject questObject in PlayerLevel5angelquest)
            {
                questObject.SetActive(true);
            }
            foreach (GameObject questObject in PlayerLevel5evilquest)
            {
                questObject.SetActive(false);
            }
        }
        else
        {
            foreach (GameObject questObject in PlayerLevel5evilquest)
            {
                questObject.SetActive(true);
            }
            foreach (GameObject questObject in PlayerLevel5angelquest)
            {
                questObject.SetActive(false);
            }
        }
    }

    public void UpdateQuest()
    {
        Level1Quest();
        LevelUp_Quest_open();
    }
}
