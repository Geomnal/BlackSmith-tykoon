using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
public class PlayerManager : MonoBehaviour
{
    public static PlayerManager instance;
    private UIManager uimanager;
    public int brokenSword = 0;
    public int reputation = 0;
    public int gold = 1500;
    public int morality = 50;
    public int Playerlevel = 1;

    public float bgmVolume = 1f; // 브금 볼륨 (0~1)

    public int requiredGold = 0;
    public int requiredReputation = 0;
    public List<int> hammer_have;    
    

    Resource resource;
    [SerializeField]
    private QuestSettingManager questSettingManager;

    public hammerdata hammerdata;
    public invenmanager invenmanager;

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject); // 씬이 바뀌어도 유지
        }
        else
        {
            Destroy(gameObject); // 이미 인스턴스가 존재하면 새로 생긴 객체를 파괴

        }
        uimanager = UIManager.instance;
    }
    private void Start()
    {
        
        if (uimanager != null)
        {
            uimanager.UpdatePlayerUI();
        }
        UpdatebrokenswordUI();
        
        Leveluptrigger();

    }
    private void Update()
    {
        uimanager = FindObjectOfType<UIManager>();
        questSettingManager = FindObjectOfType<QuestSettingManager>();
    }

    public bool PlayerLevelCheck(int level)
    {
        if(level <= Playerlevel)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    public hammerdata CurrentHammerData
    {
        get => hammerdata; 
        set
        {
            if (value != null) 
            {
                hammerdata = value;
                OnHammerDataChanged(); 
                Debug.Log($"망치 변경: {value.hammer_name}");
            }
            else
            {
                Debug.LogWarning("Value가 null입니다. ");
            }
        }
    }
    private void OnHammerDataChanged()
    {
        // 예: UI 업데이트, 다른 오브젝트에 데이터 전달 등
        Debug.Log($"Hammer success rate: {hammerdata.hammer_base_successRate}");
    }
    //플레이어 골드 증가 함수
    public void AddGold(int add_gold)
    {
        gold = gold + add_gold;
        Debug.Log($"현재 골드 : {gold}");
        Soundmanager.instance.PlayGoldsound();
    }
    //플레이어 골드 지불 함수
    public void removeGold(int remove_gold)
    {
        gold = gold - remove_gold;
        Debug.Log($"현재 골드 : {gold}");
    }
    //플레이어 명성치 지급 함수
    public void Addreputation(int add_reputation)
    {
        reputation =reputation + add_reputation;
        Debug.Log($"현재 명성치 : {reputation}");
    }
    // 플레이어 자원 관리하는 함수 절대 건들지 말 것
    public void AddResources_in_Player(int ironAmount, int woodAmount,int GoldAmount,int tungstenAmount)
    {
        ResourceManager.instance.AddResource("철", 100, ironAmount);
        ResourceManager.instance.AddResource("나무", 50, woodAmount);
        ResourceManager.instance.AddResource("금", 20, GoldAmount);
        ResourceManager.instance.AddResource("텅스텐", 20, tungstenAmount);
        Debug.Log($"Player 자원 상태: 철: {ResourceManager.instance.GetResourceAmount("철")}, 나무: {ResourceManager.instance.GetResourceAmount("나무")}");
        uimanager.UpdatePlayerUI();
    }

    public void FindUimanager()
    {
        uimanager = FindObjectOfType<UIManager>();
    }
    public void ChangeMorality(int add_Morality)
    {
        morality = Mathf.Clamp(morality + add_Morality, 0, 100);
        uimanager.UpdatePlayerUI();
        Debug.Log("선악도 변경 완료 현재 : " + morality);
        UpdateMoralityText();
        questSettingManager.moralty_up_Quest_open_level2();
    }
    public void MadeWeapon(Itemdata itemdata)
    {
        bool hasEnoughIron = ResourceManager.instance.GetResourceAmount("철") >= itemdata.requiredIron;
        bool hasEnoughWood = ResourceManager.instance.GetResourceAmount("나무") >= itemdata.requiredWood;
        bool hasEnoughGold = ResourceManager.instance.GetResourceAmount("금") >= itemdata.requiredGolds;
        bool hasEnoughTungsten = ResourceManager.instance.GetResourceAmount("텅스텐") >= itemdata.requiredTungsten;
        if (hasEnoughIron && hasEnoughWood && hasEnoughGold&& hasEnoughTungsten)
        {
            ResourceManager.instance.UseResource("철", itemdata.requiredIron);
            ResourceManager.instance.UseResource("나무", itemdata.requiredWood);
            ResourceManager.instance.UseResource("금", itemdata.requiredGolds);
            ResourceManager.instance.UseResource("텅스텐", itemdata.requiredTungsten);

            double successRate = CalculateSuccessRate(itemdata.successRate);
            if (TryCraft(successRate))
            {
                Weapon_in_invenmanager(itemdata); // itemdata를 이용하여 성공 처리
                Debug.Log($"{itemdata.itemname} 제작 성공!");
                if (uimanager != null)
                {
                    uimanager.WeaponMadeend.SetActive(true);
                }
                else
                {
                    uimanager = FindObjectOfType<UIManager>();
                    uimanager.WeaponMadeend.SetActive(true);
                }

                uimanager.UpdatePlayerUI();
            }
            else
            {
                Debug.Log("제작 실패. 부러진 검 획득.");
                if (uimanager != null)
                {
                    uimanager.Weaponmade_failed.SetActive(true);
                }
                else
                {
                    uimanager = FindObjectOfType<UIManager>();
                    uimanager.Weaponmade_failed.SetActive(true);
                }
                brokenSword = brokenSword + 1;
                UpdatebrokenswordUI();

            }
        }
        else
        {
            Debug.Log("재료가 부족합니다.");
            uimanager.Weaponmadefailed.SetActive(true);
        }
    }
    public void Weapon_in_invenmanager(Itemdata itemdata)
    {
        if (invenmanager != null)
        {
            invenmanager.IncreaseItemCount(itemdata);
            Debug.Log("현재 무기 이름은 " + itemdata.name+" 입니다");
            uimanager.weaponNameText.text = itemdata.name;

            Debug.Log("InvenManager의 IncreaseIronSwordCount 호출됨");
        }
    }
    private double CalculateSuccessRate(double baseRate) // 강화 확률 = 기본 강화 확률 + 대장장이 레벨 + 망치에 붙은 강화 확률
    {
        return baseRate + Playerlevel * 2 + hammerdata.hammer_base_successRate;
    }
    // 랜덤으로 숫자 0~100을 뽑은 후 그 결과물을 return하는 함수
    private bool TryCraft(double successRate)
    {
        double randomValue = Random.Range(0, 101);
        Debug.Log("뽑힌 랜덤 밸류 : " + randomValue);
        return randomValue < successRate;
    }
    public void LevelupButtonclick() //levelupbutton onclick
    {
        if (reputation >= requiredReputation && gold >= requiredGold)
        {
            gold = gold - requiredGold;
            Playerlevel = Playerlevel + 1;
            UpdateUI();
            questSettingManager.LevelUp_Quest_open();
            Debug.Log("레벨업 완료!");
        }
        else
        {
            Debug.Log("재료 부족");
        }
    }
    public void Levelup_For_programer()
    {
        Playerlevel = Playerlevel + 1;
        questSettingManager.LevelUp_Quest_open();
        Leveluptexttrigger();
        UpdateUI();
    }
    public void ShowWeaponSuccessRate(Itemdata itemdata, TextMeshProUGUI successRateText) // 성공 확률 보여주는 함수
    {
        if (successRateText == null)
        {
            return;
        }
        
        double successRate = CalculateSuccessRate(itemdata.successRate); // 성공 확률 계산하는 함수 사용해 성공 확률 입력
        if(successRate > 100) //100% 넘을 시 100으로 표기.
        {
            successRate = 100;
        }
        successRateText.text = $"강화 확률: {successRate}%";
    }
    private void Leveluptexttrigger()
    {
        if (uimanager != null)
        {
            uimanager.UpdatePlayerUI();
        }
    }
    private void Leveluptrigger() // 레벨 필요 요구 함수. case에 들어가는건 playerlevel
    {
        switch (Playerlevel)
        {
            case 1:
                requiredGold = 10000;
                requiredReputation = 1000;
                break;
            case 2:
                requiredGold = 15000;
                requiredReputation = 5000;
                break;
            case 3:
                requiredGold = 25000;
                requiredReputation = 10000;
                break;
            case 4:
                requiredGold = 50000;
                requiredReputation = 35000;
                break;
            case 5:
                requiredGold = 100000;
                requiredReputation = 50000;
                break;
            // 레벨에 따른 추가 조건을 추가하세요.
            default:
                requiredGold = 100000;
                requiredReputation = 50000;
                break;
        }
    }
    public void UpdateMoralityText()
    {
        uimanager.UpdatePlayerUI();
    }
    public void UpdateUI()
    {
        if (uimanager != null)
        {
            uimanager.UpdatePlayerUI();
        }
        
        Leveluptrigger();
        Leveluptexttrigger();
    }
    public void UpdatebrokenswordUI()
    {
        uimanager.UpdatePlayerUI();
    }
}




public class Weaponingredient
{
    public string i_name;
    public int price;

    public Weaponingredient(string i_name, int price)
    {
        this.i_name = i_name;
        this.price = price;
    }
}
