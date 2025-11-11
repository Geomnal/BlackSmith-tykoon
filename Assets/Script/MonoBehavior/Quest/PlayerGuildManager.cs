using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using System.Runtime.CompilerServices;


#if UNITY_EDITOR
using UnityEditor;
using static UnityEditor.Progress;
#endif

public class PlayerGuildManager : MonoBehaviour
{
    protected invenmanager inven;
    protected PlayerManager playerManager;

    public int player_buycount; // 플레이어 구매 카운트용 변수
    public List<TextMeshProUGUI> playerBuycountTexts; // 상점 카운트 텍스트들

    [SerializeField] private List<TextMeshProUGUI> quest_reward_Texts; // Text UI 요소를 리스트로 선언

    protected List<int> quest_complete_reward = new List<int>()
    {
        1000,1500,3200,500,2500,5000,5700,4000,8000,6000,9000,10000,20000,15000,15000,25000,30000
    };
    protected List<string> questtext_list = new List<string>();

    void Start()
    {
        playerManager = PlayerManager.instance;
        if (playerManager == null)
        {
            Debug.LogError("PlayerManager를 찾을 수 없습니다.");
        }

        // FindObjectOfType로 invenmanager 가져오기
        inven = FindObjectOfType<invenmanager>();
        if (inven == null)
        {
            Debug.LogError("invenmanager를 찾을 수 없습니다.");
        }
        if (quest_complete_reward.Count > 0)
        {
            QuestTextsetting();
        }
        else
        {
            Debug.LogError("quest_complete_reward 리스트가 비어 있습니다.");
        }

        if (inven == null)
        {
            Debug.LogError("PlayerGuildManager를 찾을 수 없습니다.");
        }

    }
    private void Update()
    {
        Textupdate();
        FindObject();
    }
    private void FindObject()
    {
        inven = invenmanager.instance;
        playerManager = PlayerManager.instance;
    }
    public void BuyItem(string resourceName)
    {
        Resource resource;
        if (ResourceManager.instance.resources.ContainsKey(resourceName))
        {
            resource = ResourceManager.instance.resources[resourceName];
        }
        else
        {
            resource = null;
        }

        if (resource == null)
        {
            Debug.LogWarning("해당 자원이 ResourceManager에 없습니다.");
            return;
        }


        // 총 구매 비용 계산
        int totalCost = resource.price * player_buycount;

        // 플레이어의 골드가 충분한지 확인
        if (playerManager.gold >= totalCost)
        {
            // 골드 감소 및 아이템 지급
            playerManager.gold -= totalCost;
            ResourceManager.instance.AddResource(resourceName, resource.price, player_buycount); 
            Debug.Log($"{resourceName}을(를) {player_buycount}개 구매하였습니다. 남은 골드: {playerManager.gold}");
            player_buycount = 0;
        }
        else
        {
            // 골드가 부족할 때
            Debug.Log("골드가 부족하여 구매할 수 없습니다.");
            return;
        }
    }
    private void AddItemToPlayerInventory(string itemName, int count)
    {
        if (ResourceManager.instance != null)
        {
            ResourceManager.instance.AddResource(itemName, 0, count);
        }
        else
        {
            Debug.LogError("ResourceManager를 찾을 수 없습니다.");
        }
    }
    public void LevelupButtonClick()
    {
        playerManager.LevelupButtonclick();
    }
    public void LevelupbuttonClick_for_programer()
    {
        playerManager.Levelup_For_programer();
    }
    public void QuestComplete(Quest_class questRequirements, int rewardGold, int rewardReputation, int moralityChange) //퀘스트 완료하는 함수.
    {
        bool requirementsMet = true;

        if (!string.IsNullOrEmpty(questRequirements.item_name_1) && inven.itemCounts.ContainsKey(questRequirements.item_name_1)) //널처리
        {
            if (inven.itemCounts[questRequirements.item_name_1] < questRequirements.item_1)
            {
                requirementsMet = false;
            }
        }

        if (!string.IsNullOrEmpty(questRequirements.item_name_2) && inven.itemCounts.ContainsKey(questRequirements.item_name_2)) //널처리
        {
            if (inven.itemCounts[questRequirements.item_name_2] < questRequirements.item_2)
            {
                requirementsMet = false;
            }
        }

        if (!string.IsNullOrEmpty(questRequirements.item_name_3) && inven.itemCounts.ContainsKey(questRequirements.item_name_3)) //널처리
        {
            if (inven.itemCounts[questRequirements.item_name_3] < questRequirements.item_3)
            {
                requirementsMet = false;
            }
        }

        if (requirementsMet)
        {
            // 보상 제공
            playerManager.AddGold(rewardGold);
            playerManager.Addreputation(rewardReputation);
            playerManager.ChangeMorality(moralityChange);

            // 아이템 차감
            if (!string.IsNullOrEmpty(questRequirements.item_name_1)) // 널처리
                inven.itemCounts[questRequirements.item_name_1] -= questRequirements.item_1; 

            if (!string.IsNullOrEmpty(questRequirements.item_name_2)) // 널처리
                inven.itemCounts[questRequirements.item_name_2] -= questRequirements.item_2;

            if (!string.IsNullOrEmpty(questRequirements.item_name_3)) // 널처리
                inven.itemCounts[questRequirements.item_name_3] -= questRequirements.item_3;

            Debug.Log("퀘스트 완료! 보상을 받았습니다.");
            inven.UpdateUI();
            playerManager.UpdateUI();
        }
        else
        {
            Debug.Log("퀘스트 완료 조건을 충족하지 못했습니다.");
        }
    }

    public void IncreaseBuyCount()
    {
        player_buycount = player_buycount + 1;
        Debug.Log($"현재 구매 수량: {player_buycount}");
    }
    public void DecreaseBuyCount()
    {
        if (player_buycount > 0)
        {
            player_buycount -= 1;
            Debug.Log($"현재 구매 수량: {player_buycount}");
        }
        else
        {
            Debug.Log("구매 수량은 0보다 적을 수 없습니다.");
        }
    }
    public void ironbuy()
    {
        BuyItem("철");
    }
    public void woodbuy()
    {
        BuyItem("나무");
    }
    public void adventureTicketbuy()
    {
        BuyItem("탐험 허가증");
    }
    public void Textupdate()
    {
        if (playerBuycountTexts != null && playerBuycountTexts.Count > 0)
        {
            foreach (TextMeshProUGUI text in playerBuycountTexts)
            {
                if(text != null)
                {
                    text.text = $"{player_buycount}";
                }
                
            }
        }
    }

    public void QuestPotal(int Quest)
    {
        switch(Quest)
        {
            case 1:
                Quest1Complete();
                break;
            case 2: 
                Quest2Complete(); 
                break;
            case 3: 
                Quest3Complete();
                break;
            case 4: 
                Quest4Complete();
                break;
            case 5:
                Quest5Complete();
                break;
            case 6:
                Quest6Complete();
                break;
            case 7:
                Quest7Complete();
                break;
            case 8:
                Quest8Complete();
                break;
            case 9:
                Quest9Complete();
                break;
            case 10:
                Quest10Complete();
                break;
            case 11:
                Quest11Complete();
                break;
            case 12:
                Quest12Complete();
                break;
            case 13:
                Quest13Complete();
                break;
            case 14:
                Quest14Complete();
                break;
            case 15:
                Quest15Complete();
                break;
            case 16:
                Quest16Complete();
                break;
            case 17:
                Quest17Complete();
                break;
            default:
                Debug.Log("스위치 문에 추가가 안됐는디요?");
                break;

        }
    }
    /// <summary>
    /// 레벨 1
    /// </summary>
    private void Quest1Complete()
    {
        Quest_class quest1 = new Quest_class { item_name_1 = "철 검", item_1 = 2 };
        QuestComplete(quest1, quest_complete_reward[0], 100, 1);

    }
    private void Quest2Complete()
    {
        Quest_class quest2 = new Quest_class { item_name_1 = "철 검", item_name_2 = "철 갑옷", item_1 = 2, item_2 = 1 };
        QuestComplete(quest2, quest_complete_reward[1], 100, 1);
    }
    private void Quest3Complete()
    {
        Quest_class quest3 = new Quest_class { item_name_1 = "철 검", item_name_2 = "철 갑옷", item_1 = 4, item_2 = 1 };
        int QuestMaxGold = quest_complete_reward[2] + 1;
        int QuestGold = Random.Range(1600, QuestMaxGold);
        QuestComplete(quest3, QuestGold, 100, -3);
    }
    private void Quest4Complete()
    {
        if(playerManager.brokenSword >= 10)
        {
            playerManager.brokenSword = playerManager.brokenSword - 10;
            playerManager.AddGold(quest_complete_reward[3]);
        }
        else
        {
            Debug.Log("부러진 검 부족");
        }

        playerManager.UpdatebrokenswordUI();
    }
    /// <summary>
    /// 레벨 2
    /// </summary>
    private void Quest5Complete()
    {
        Quest_class quest = new Quest_class { item_name_1 = "나무 검", item_name_2 = "철 괭이", item_1 = 2, item_2 = 1 };
        QuestComplete(quest, quest_complete_reward[4], 100, 1);
    }
    private void Quest6Complete()
    {
        Quest_class quest = new Quest_class { item_name_1 = "철 검", item_name_2 = "철 창",item_name_3 = "철 방패" ,item_1 = 4, item_2 = 2 ,item_3 = 1};
        QuestComplete(quest, quest_complete_reward[5], 300, 1);
    }
    private void Quest7Complete()
    {
        Quest_class quest = new Quest_class { item_name_1 = "철 검", item_name_2 = "철 창",  item_1 = 4, item_2 = 1, };
        int QuestMaxGold = quest_complete_reward[6] + 1;
        int QuestGold = Random.Range(3200, QuestMaxGold);
        QuestComplete(quest, quest_complete_reward[6], 100, -3);
    }
    /// <summary>
    /// 레벨 3
    /// </summary>
    private void Quest8Complete()
    {
        //고대의 수호자
        Quest_class quest = new Quest_class { item_name_1 = "강철 검", item_name_2 = "철 검 묶음", item_1 = 1, item_2 = 1, };
        QuestComplete(quest, quest_complete_reward[7], 100, 1);

    }
    private void Quest9Complete()
    {
        //산적 두목 로드릭
        Quest_class quest = new Quest_class { item_name_1 = "강철 검", item_name_2 = "철 갑옷", item_1 = 2, item_2 = 1, };
        int QuestMaxGold = quest_complete_reward[8] + 1;
        int QuestGold = Random.Range(3500, QuestMaxGold);
        QuestComplete(quest, QuestGold, 100, -3);
    }
    private void Quest10Complete()
    {
        //황제의 근위대장 프리드릭
        Quest_class quest = new Quest_class { item_name_1 = "강철 검", item_name_2 = "은 목걸이", item_1 = 2, item_2 = 1, };
        QuestComplete(quest, quest_complete_reward[9], 100, 2);
    }
    private void Quest11Complete()
    {
        //암흑의 마법사 자칼
        Quest_class quest = new Quest_class { item_name_1 = "강철 검", item_name_2 = "은 목걸이", item_1 = 4, item_2 = 1, };
        int QuestMaxGold = quest_complete_reward[10] + 1;
        int QuestGold = Random.Range(4000, QuestMaxGold);
        QuestComplete(quest, QuestGold, 100, -3);
    }
    /// <summary>
    /// 레벨 4
    /// </summary>
    private void Quest12Complete()
    {
        //신성한 결혼식
        Quest_class quest = new Quest_class { item_name_1 = "금 갑옷", item_name_2 = "금 목걸이", item_1 = 1, item_2 = 1, };
        QuestComplete(quest, quest_complete_reward[11], 100, 1);
    }
    private void Quest13Complete()
    {
        //어둠의 의식
        Quest_class quest = new Quest_class { item_name_1 = "강철 검", item_name_2 = "금 목걸이", item_name_3 = "마검 - 사라트", item_1 = 1, item_2 = 1, item_3 = 1 };
        int QuestMaxGold = quest_complete_reward[12] + 1;
        int QuestGold = Random.Range(11000, QuestMaxGold);
        QuestComplete(quest, QuestGold, 100, -3);
    }
    private void Quest14Complete()
    {
        //왕의 최후 방어선
        Quest_class quest = new Quest_class { item_name_1 = "금 갑옷", item_name_2 = "금 목걸이", item_name_3 = "철 방패", item_1 = 1, item_2 = 1, item_3 = 1};
        QuestComplete(quest, quest_complete_reward[13], 100, 1);
    }
    private void Quest15Complete()
    {
        //마검의 계승자
        Quest_class quest = new Quest_class { item_name_1 = "마검 - 사라트", item_1 = 1 };
        int QuestMaxGold = quest_complete_reward[14] + 1;
        int QuestGold = Random.Range(7000, QuestMaxGold);
        QuestComplete(quest, QuestGold, 100, -3);
    }
    /// <summary>
    /// 레벨 5
    /// </summary>
    private void Quest16Complete()
    {
        //빛의 계승자
        Quest_class quest = new Quest_class { item_name_1 = "마검 - 삼위일체", item_1 = 1 };
        QuestComplete(quest, quest_complete_reward[15], 100, 1);
    }
    private void Quest17Complete()
    {
        //파괴의 사자
        Quest_class quest = new Quest_class { item_name_1 = "마검 - 본다르", item_1 = 1 };
        int QuestMaxGold = quest_complete_reward[16] + 1;
        int QuestGold = Random.Range(3200, QuestMaxGold);
        QuestComplete(quest, QuestGold, 100, -3);
    }
    private void QuestTextsetting()
    {
        questtext_list = new List<string>()
        {
            "사례금 : "+quest_complete_reward[0]+"골드", "사례금 : "+quest_complete_reward[1]+"골드", "사례금 : 1600~"+quest_complete_reward[2]+"골드",
            "사례금 : "+quest_complete_reward[3]+"골드", "사례금 : "+quest_complete_reward[4]+"골드", "사례금 : "+quest_complete_reward[5]+"골드",
            "사례금 : 3200~"+quest_complete_reward[6]+"골드", "사례금 : "+quest_complete_reward[7]+"골드", "사례금 : 3500~"+quest_complete_reward[8]+"골드",
            "사례금 : "+quest_complete_reward[9]+"골드", "사례금 : 4000~"+quest_complete_reward[10]+"골드", "사례금 : "+quest_complete_reward[11]+"골드",
            "사례금 : 11000~"+quest_complete_reward[12]+"골드", "사례금 : "+quest_complete_reward[13]+"골드", "사례금 : 7000~"+quest_complete_reward[14]+"골드",
            "사례금 : "+quest_complete_reward[15]+"골드", "사례금 : 7000~"+quest_complete_reward[16]+"골드"
        };

        for (int i = 0; i < quest_reward_Texts.Count && i < questtext_list.Count; i++)
        {
            if (quest_reward_Texts[i] != null)
            {
                quest_reward_Texts[i].text = questtext_list[i];
            }
        }
    }

}

public class Quest_class
{
    public int item_1;
    public int item_2;
    public int item_3;

    public string item_name_1;
    public string item_name_2;
    public string item_name_3;
}
