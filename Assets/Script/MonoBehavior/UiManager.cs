using System.Collections.Generic;
using UnityEngine;
using TMPro;
using System.Resources;
using UnityEngine.UI;
using Unity.VisualScripting;

public class UIManager : MonoBehaviour
{
    public static UIManager instance;
    public PlayerManager playerManager;
    private invenmanager invenmanager;
    private ResourceManager resourcemanager;
    public Button saveButton;
    public Button loadButton;
    public DataManager dataManager;

    private int i_ironclickcount = 10;
    private int i_woodclickcount = 10;

    public Slider moralitybar;

    public GameObject WeaponMadeend; //무기 제작 완료했을 때 띄우는 게임 오브젝트
    public GameObject Weaponmadefailed; // 무기 제작 실패했을때 ( 재료 없을 때 ) 띄우는 게임 오브젝트
    public GameObject Weaponmade_failed; // 무기 제작 실패했을 때 ( 확률로 인해 ) 띄우는 게임 오브젝트

    // PlayerManager 텍스트 UI 변수
    [SerializeField] private List<TextMeshProUGUI> playerReputationTexts; //명성치 텍스트
    [SerializeField] private List<TextMeshProUGUI> playerBrokenSwordTexts; //부서진 검 표기 텍스트
    [SerializeField] private TextMeshProUGUI goldText; //플레이어 재화 표기 텍스트
    public TextMeshProUGUI angelText; //플레이어 선 표기 텍스트
    public TextMeshProUGUI evilText; // 플레이어 악 표기 텍스트
    [SerializeField] private TextMeshProUGUI playerLevelText; //플레이어 레벨 텍스트
    [SerializeField] private TextMeshProUGUI playerLevelUpGoldText; //플레이어 레벨 업시 필요한 골드 출력 텍스트
    [SerializeField] private TextMeshProUGUI playerLevelUpRequiredText; //플레이어 레벨 업시 필요한 requiredtext 출력 텍스트..
    public TextMeshProUGUI weaponNameText;
    [SerializeField] private TextMeshProUGUI ironText;
    [SerializeField] private TextMeshProUGUI woodText;
    [SerializeField] private TextMeshProUGUI r_gold_Text;
    [SerializeField] private TextMeshProUGUI r_tungsten_text;
    [SerializeField] private TextMeshProUGUI adventureTicketcount;

    // invenmanager 텍스트 UI 변수
    [SerializeField]private List<TextMeshProUGUI> ironSwordTexts;
    [SerializeField]private List<TextMeshProUGUI> woodSwordTexts;
    [SerializeField]private List<TextMeshProUGUI> ironArmorTexts;
    [SerializeField]private List<TextMeshProUGUI> ironHoeTexts;
    [SerializeField]private List<TextMeshProUGUI> ironShieldTexts;
    [SerializeField]private List<TextMeshProUGUI> ironSpearTexts;
    [SerializeField]private List<TextMeshProUGUI> ironSwordsTexts;
    [SerializeField]private List<TextMeshProUGUI> silverNecklaceTexts;
    [SerializeField]private List<TextMeshProUGUI> steelSwordTexts;
    [SerializeField] private List<TextMeshProUGUI> GoldNecklaceTexts;
    [SerializeField] private List<TextMeshProUGUI> GoldArmorTexts;
    [SerializeField] private List<TextMeshProUGUI> magicsword_saratTexts;
    [SerializeField] private List<TextMeshProUGUI> magicsword_trinity_force_Texts;
    [SerializeField] private List<TextMeshProUGUI> magicsword_bondar_Texts;
    [SerializeField] private List<TextMeshProUGUI> magicsword_al_bansar_Texts;


    // ResourceManager 텍스트 UI 변수
    [SerializeField] private TextMeshProUGUI ironClickCountText;
    [SerializeField] private TextMeshProUGUI woodClickCountText;

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
    private void Start()
    {
        Findobject();

        if (playerManager == null || invenmanager == null || resourcemanager == null)
        {
            Debug.LogError("PlayerManager, InvenManager 또는 ResourceManager가 초기화되지 않았습니다.");
            return;
        }
        if (dataManager == null)
        {
            dataManager = FindObjectOfType<DataManager>();  // DataManager 싱글톤 객체를 가져오거나 FindObjectOfType으로 참조
        }
        if (moralitybar == null)
        {
            moralitybar = FindObjectOfType<Slider>();
        }

        // 버튼에 동적으로 이벤트 추가
        saveButton.onClick.AddListener(dataManager.SaveData);
        loadButton.onClick.AddListener(dataManager.LoadData);
        Debug.Log($"playerManager: {playerManager}");
        Debug.Log($"playerReputationTexts Count: {playerReputationTexts.Count}");
        UpdatePlayerUI();
        UpdateInventoryUI();
    }
    private void Update()
    {
        UpdateAllUI();
    }
    private void OnEnable()
    {
        Findobject();
    }
    public void Findobject()
    {
        playerManager = PlayerManager.instance;
        invenmanager = invenmanager.instance;
        resourcemanager = ResourceManager.instance;
    }
    // 플레이어 텍스트 업데이트 함수
    public void UpdatePlayerUI()
    {
        foreach (TextMeshProUGUI text in playerReputationTexts)
        {
            if (playerReputationTexts != null || playerReputationTexts.Count != 0)
            {
                text.text = $"대장장이 명성치 : {playerManager.reputation}";
            }
            else
            {
                Debug.Log("명성치 관련 텍스트 null");
            }
        }
        foreach (TextMeshProUGUI text in playerBrokenSwordTexts)
        {
            text.text = $"보유 부러진 검 : {playerManager.brokenSword}";
        }
        moralitybar.value = playerManager.morality;

        goldText.text = $"{playerManager.gold}";
        angelText.text = $"{playerManager.morality}";
        evilText.text = $"{100 - playerManager.morality}";
        playerLevelText.text = $"플레이어 레벨: {playerManager.Playerlevel}";
        playerLevelUpGoldText.text = $"승급 시 필요한 골드 : {playerManager.requiredGold}";
        playerLevelUpRequiredText.text = $"승급 시 필요한 명성치 : {playerManager.requiredReputation}";
        
        if (ResourceManager.instance != null)
        {
            ironText.text = $"{ResourceManager.instance.GetResourceAmount("철")}";
            woodText.text = $"{ResourceManager.instance.GetResourceAmount("나무")}";
            r_gold_Text.text = $"{ResourceManager.instance.GetResourceAmount("금")}";
            r_tungsten_text.text = $"{ResourceManager.instance.GetResourceAmount("텅스텐")}";
            if (adventureTicketcount != null)
            {
                adventureTicketcount.text = $"가지고 있는 탐험 허가증 : {ResourceManager.instance.GetResourceAmount("탐험 허가증")}";
            }
        }
    }

    // 인벤토리 텍스트 업데이트 함수
    public void UpdateInventoryUI()
    {
        foreach (TextMeshProUGUI text in ironSwordTexts)
        {
            text.text = $"보유 철 검 : {invenmanager.itemCounts["철 검"]}";
        }
        foreach (TextMeshProUGUI text in woodSwordTexts)
        {
            text.text = $"보유 나무 검 : {invenmanager.itemCounts["나무 검"]}";
        }
        foreach (TextMeshProUGUI text in ironArmorTexts)
        {
            text.text = $"보유 철 갑옷 : {invenmanager.itemCounts["철 갑옷"]}";
        }
        foreach (TextMeshProUGUI text in ironHoeTexts)
        {
            text.text = $"보유 철 괭이 : {invenmanager.itemCounts["철 괭이"]}";
        }
        foreach (TextMeshProUGUI text in ironShieldTexts)
        {
            text.text = $"보유 철 방패 : {invenmanager.itemCounts["철 방패"]}";
        }
        foreach (TextMeshProUGUI text in ironSpearTexts)
        {
            text.text = $"보유 철 창 : {invenmanager.itemCounts["철 창"]}";
        }
        foreach (TextMeshProUGUI text in ironSwordsTexts)
        {
            text.text = $"철 검 묶음 : {invenmanager.itemCounts["철 검 묶음"]}";
        }
        foreach (TextMeshProUGUI text in silverNecklaceTexts)
        {
            text.text = $"보유 은 목걸이 : {invenmanager.itemCounts["은 목걸이"]}";
        }
        foreach (TextMeshProUGUI text in steelSwordTexts)
        {
            text.text = $"보유 강철 검 : {invenmanager.itemCounts["강철 검"]}";
        }
        foreach (TextMeshProUGUI text in GoldNecklaceTexts)
        {
            text.text = $"보유 금 목걸이 : {invenmanager.itemCounts["금 목걸이"]}";

        }
        foreach (TextMeshProUGUI text in GoldArmorTexts)
        {
            text.text = $"보유 금 갑옷 : {invenmanager.itemCounts["금 갑옷"]}";
        }
        foreach (TextMeshProUGUI text in magicsword_saratTexts)
        {
            text.text = $"마검 사라트 : {invenmanager.itemCounts["마검 - 사라트"]}";
        }
        foreach (TextMeshProUGUI text in magicsword_bondar_Texts)
        {
            text.text = $"마검 본다르 : {invenmanager.itemCounts["마검 - 본다르"]}";
        }
        foreach (TextMeshProUGUI text in magicsword_trinity_force_Texts)
        {
            text.text = $"마검 삼위일체 : {invenmanager.itemCounts["마검 - 삼위일체"]}";
        }
        foreach (TextMeshProUGUI text in magicsword_al_bansar_Texts)
        {
            text.text = $"마검 알 반살 : {invenmanager.itemCounts["마검 - 알 반살"]}";
        }


    }
    public void owner_iron()
    {
        if (i_ironclickcount == 1)
        {
            PlayerManager.instance.AddResources_in_Player(3, 0,0,0);
            i_ironclickcount = 10;
            UpdateResourceUI();
            Soundmanager.instance.Playbreakstonesound();
        }
        else
        {
            i_ironclickcount = i_ironclickcount - 1;
            UpdateResourceUI();
            Soundmanager.instance.Playhitstonesound();
        }
    }
    public void owner_wood()
    {
        if (i_woodclickcount == 1)
        {
            PlayerManager.instance.AddResources_in_Player(0, 3, 0, 0);
            i_woodclickcount = 10;
            Soundmanager.instance.Playbreakwoodsound();
        }
        else
        {
            i_woodclickcount = i_woodclickcount - 1;
            Soundmanager.instance.Playhitwoodsound();
        }
    }
    public void For_Programer()
    {
        playerManager.AddResources_in_Player(10, 10, 10, 10 ); // 자원 획득 확인용으로 둔 함수, 추후 탐색으로 수정 할 예정이니 일단 보류.
    }
    // 자원 텍스트 업데이트 함수
    public void UpdateResourceUI()
    {
        ironClickCountText.text = $"철 광석 채취까지 : {i_ironclickcount}";
        woodClickCountText.text = $"나무 목재 채취까지 : {i_woodclickcount}";
    }
    public void UpdateAllUI()
    {
        if (playerManager != null)
        {
            UpdatePlayerUI();
        }
        if (invenmanager != null)
        {
            UpdateInventoryUI();
        }
        if (resourcemanager != null)
        {
            UpdateResourceUI();
        }
    }
}


