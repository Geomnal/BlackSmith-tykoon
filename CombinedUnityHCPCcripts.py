# --- File: Assets\Script\adventure_game_manager\adventure.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class adventure : MonoBehaviour
{
    //수업중 나온 말 abstract << 부모 클래스는 선언만, 구현은 자식 클래스에서
    // virtual << 부모 클래스에서 선언, 구현 동시 가능하나 계승할지 계승(아서스버전) 할 지는 자식 클래스의 몫.




    protected int playerHealth = 0;
    protected int baseIron = 5;
    protected int baseWood = 5;
    protected int baseresource = 0;
    protected int baseironsword = 0;

    [SerializeField]private ResourceManager resourceManager;


    protected bool owngold = false;
    protected bool owntungsten = false;

    private void Update()
    {
        resourceManager = ResourceManager.instance;
    }
    public void GrantBaseResources()
    {
        if (resourceManager != null)
        {
            resourceManager.AddResource("철", 0, baseIron);
            resourceManager.AddResource("나무", 0, baseWood);
            Debug.Log($"기본 자원 지급: 철 {baseIron}개, 나무 {baseWood}개");

        }
        // 리소스 매니저를 통해 자원을 추가

    }
    public virtual void EndAdventure()
    {

        GrantBaseResources();
        owngold = randomresource(baseresource);
        owntungsten = randomresource(baseresource);
        if(owngold)
        {
            resourceManager.AddResource("금", 0, 1);
        }
        if(owntungsten)
        {
            resourceManager.AddResource("텅스텐", 0, 1);
        }
        // 추가적인 탐사 로직은 자식 클래스에서 구현
    }
    public bool randomresource(int successrate)
    {
        int Randomvalue = Random.Range(0, 101);
        if(Randomvalue <= successrate)
        {
            return true;
        }
        else
        {
            return false;
        }
    }



}


# --- File: Assets\Script\adventure_game_manager\CardDrawnManager.cs ---
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
public class CardGameManager : adventure
{
    // 플레이어의 초기 체력
    public TextMeshProUGUI playerHealthText; // 플레이어 체력 UI
    public TextMeshProUGUI playerturnendText; // 플레이어 체력 UI

    public QuestSettingManager questSettingManager;

    public TextMeshProUGUI ownironText; // 플레이어 체력 UI
    public TextMeshProUGUI ownwoodText; // 플레이어 체력 UI
    public TextMeshProUGUI owngoldText; // 플레이어 체력 UI
    public TextMeshProUGUI owntungstenText;
    public TextMeshProUGUI ownironswordText;


    public GameObject PlayerTurnendobject;
    public GameObject Playeradventureendobject;

    public List<GameObject> cards; // 스크롤 뷰 내 카드 리스트 (각각의 카드 프리팹이 들어가야 함)
    public List<GameObject> card_information; // 카드 정보 보여주는 게임 오브젝트들

    public int maxDrawsPerTurn = 1; // 턴당 드로우 가능한 최대 카드 수
    private HashSet<int> drawnCards = new HashSet<int>(); // 이미 드로우된 카드 인덱스를 저장하는 HashSet
    private int currentTurnDraws = 0; // 현재 턴에서 드로우된 카드 수

    private bool isFirstTurn = true; // 첫 턴인지 여부 확인
    private bool isPlayerTurn = true; // 현재 플레이어 턴인지 여부

    private PlayerManager playerManager;
    private ResourceManager resourceManager;
    private invenmanager inven;

    public GameObject Card1_imp;
    public GameObject Card2_imp;
    public GameObject Card3_imp;
    public GameObject Card4_imp;
    public GameObject Card5_imp;

    public List<GameObject> card1List; // 1번 카드 리스트
    public List<GameObject> card2List; // 2번 카드 리스트
    public List<GameObject> card3List; // 3번 카드 리스트
    public List<GameObject> card4List; // 4번 카드 리스트
    public List<GameObject> card5List; // 5번 카드 리스트

    private void Start()
    {
        playerManager = PlayerManager.instance;
        inven = invenmanager.instance;
        questSettingManager = QuestSettingManager.instance;
        InitializeCards();
        UpdatePlayerHealthUI();
        if (isFirstTurn)
        {
            DrawCards(3); // 첫 턴에는 3장 드로우
            isFirstTurn = false; // 첫 턴 이후로 변경
        }
    }

    // 카드 초기화 - 모든 카드를 비활성화 상태로 설정
    private void InitializeCards()
    {
        foreach (GameObject card in cards)
        {
            card.SetActive(false);
        }
    }
    private void DrawSingleCard()
    {
        int cardIndex = GetUniqueRandomCardIndex();

        if (cardIndex != -1) // 유효한 카드 인덱스가 반환되었을 때만
        {
            cards[cardIndex].SetActive(true); // 카드 활성화
            drawnCards.Add(cardIndex); // 드로우된 카드 인덱스 저장
            currentTurnDraws++; // 현재 턴 드로우 수 증가
        }
        else
        {
            Debug.Log("드로우 가능한 카드가 없습니다.");
        }
    }
    private void EnemyTurn()
    {

        int damage = GetRandomEnemyCardDamage(); // 랜덤하게 피로도 값을 얻음
        playerturnendText.text = $"하루가 지났습니다. 플레이어의 피로도가 {damage}만큼 증가합니다.(피로도가 100이상 되었을 시 플레이어는 귀환합니다.";
        PlayerTurnendobject.SetActive(true);
        playerHealth = playerHealth + damage; // 플레이어 피로도 증가
        if (playerHealth > 100)
        {
            playerHealth = 100;
        }
        Debug.Log($"하루가 지나 {damage} 만큼 피로도가 증가했습니다.");

        UpdatePlayerHealthUI();

        // 플레이어 체력이 0 이상이 되면 탐색 종료
        if (playerHealth >= 100)
        {

            EndExploration();
            EndAdventure();
        }
        else
        {
            isPlayerTurn = true; // 다시 플레이어 턴으로 전환
        }
    }
    private void UpdatePlayerHealthUI()
    {
        if (playerHealthText != null)
        {
            playerHealthText.text = $"피로도: {playerHealth}";
        }
    }
    private void EndExploration()
    {
        Debug.Log("탐색이 종료되었습니다. 플레이어가 패배했습니다.");
        // 탐색 종료 UI 표시 등의 추가 작업 수행
    }
    private int GetRandomEnemyCardDamage()
    {
        // 예시로 랜덤 데미지를 10~30 사이로 설정
        return Random.Range(10, 31);
    }
    public void DrawCards(int count)
    {
        int drawsThisTurn = 0;
        while (drawsThisTurn < count)
        {
            DrawSingleCard();
            drawsThisTurn++;
        }
    }

    public void adventure_exit()
    {
        playerHealth = 100;
        Debug.Log("어드벤쳐 종료!");
        UpdatePlayerHealthUI();
        EndAdventure();
    }

    // 드로우 함수 - 버튼 클릭 시 호출
    public void DrawCard()
    {
        if (currentTurnDraws < maxDrawsPerTurn)
        {
            DrawSingleCard();
        }
        else
        {
            Debug.Log("이번 턴에 더 이상 카드를 드로우할 수 없습니다.");
        }
    }
    public void Card1()
    {
        if (isPlayerTurn)
        {
            Debug.Log("더 깊은 곳으로 사용");
            baseIron = baseIron - 2;
            baseWood = baseWood - 2;
            baseresource = baseresource + 25;
            if (baseIron < 0 || baseWood < 0)
            {
                baseIron = 0;
                baseWood = 0;
            }
        }
        EndTurn();
        RemoveRandomActiveCard(1);

    }

    public void Card2()
    {
        if (isPlayerTurn)
        {
            int randomiron = Random.Range(2, 5);
            int randomwood = Random.Range(2, 5);
            baseIron = baseIron + randomiron;
            baseWood = baseWood + randomwood;
        }
        RemoveRandomActiveCard(2);
        EndTurn();

    }
    public void Card3()
    {
        if (isPlayerTurn)
        {
            playerHealth = playerHealth - 25;
            UpdatePlayerHealthUI();
            Debug.Log("맥주 카드 사용: 추가 카드 드로우");
            DrawSingleCard(); // 추가로 한 장 더 드로우
        }
        RemoveRandomActiveCard(3);
        EndTurn();

    }
    public void Card4()
    {
        if (isPlayerTurn)
        {
            Debug.Log("전쟁의 상흔 카드 사용: 철 검 획득");
            baseironsword = baseironsword + 1;
        }
        RemoveRandomActiveCard(4);
        EndTurn();

    }

    public void Card5(int discardCount)
    {
        InitializeCards();
        if (isPlayerTurn)
        {
            int discards = 0;
            while (discards < discardCount && cards.Count > 0)
            {
                int discardIndex = GetUniqueRandomCardIndex();
                if (discardIndex != -1)
                {
                    cards[discardIndex].SetActive(false); // 카드 비활성화
                    drawnCards.Remove(discardIndex); // drawnCards에서도 제거
                    discards++;
                }
            }

            DrawCards(discardCount); // 새로 3장 드로우
        }
        Debug.Log("비장의 수 카드 사용: 3장 버리고 3장 드로우");
        RemoveRandomActiveCard(5);
        EndTurn();


    }

    // 중복되지 않은 랜덤 카드 인덱스 생성
    private int GetUniqueRandomCardIndex()
    {
        if (drawnCards.Count >= cards.Count) // 모든 카드가 이미 드로우된 경우
        {
            Debug.Log("모든 카드를 드로우했으므로 다시 덱을 섞습니다.");
            drawnCards.Clear(); // drawnCards 초기화하여 다시 드로우 가능하게 함
        }

        int randomIndex;
        do
        {
            randomIndex = Random.Range(0, cards.Count);
        } while (drawnCards.Contains(randomIndex));

        return randomIndex;
    }

    // 턴이 끝났을 때 호출하는 함수 - 다음 턴을 준비
    public void EndTurn()
    {
        if (isPlayerTurn)
        {
            currentTurnDraws = 0; // 플레이어의 턴 종료 후 드로우 초기화
            isPlayerTurn = false;
            EnemyTurn(); // 적의 턴으로 전환
        }
        foreach (GameObject cardobject in card_information)
        {
            cardobject.SetActive(false);
        }
    }

    // 게임이 새로 시작되거나 리셋되었을 때 호출하는 함수 - 카드 초기화 및 리셋
    public void ResetGame()
    {
        InitializeCards();
        drawnCards.Clear();
        currentTurnDraws = 0;
        isFirstTurn = true; // 첫 턴 상태로 복귀
    }

    public void Cardopen(int card_index)
    {
        switch (card_index)
        {
            case 1:
                Card1_imp.SetActive(true);
                break;
            case 2:
                Card2_imp.SetActive(true);
                break;
            case 3:
                Card3_imp.SetActive(true);
                break;
            case 4:
                Card4_imp.SetActive(true);
                break;
            case 5:
                Card5_imp.SetActive(true);
                break;
            default:
                break;

        }
    }
    public void CloseImp(int card_index)
    {
        switch (card_index)
        {
            case 1:
                Card1_imp.SetActive(false);
                break;
            case 2:
                Card2_imp.SetActive(false);
                break;
            case 3:
                Card3_imp.SetActive(false);
                break;
            case 4:
                Card4_imp.SetActive(false);
                break;
            case 5:
                Card5_imp.SetActive(false);
                break;
            default:
                break;

        }
    }
    public void CloseplayerTurnendObject()
    {
        PlayerTurnendobject.SetActive(false);
    }
    public void RemoveRandomActiveCard(int card_index)
    {
        List<GameObject> selectedList = null;

        // card_index에 따라 리스트 선택
        switch (card_index)
        {
            case 1:
                selectedList = card1List;
                break;
            case 2:
                selectedList = card2List;
                break;
            case 3:
                selectedList = card3List;
                break;
            case 4:
                selectedList = card4List;
                break;
            case 5:
                selectedList = card5List;
                break;
            default:
                Debug.LogWarning("잘못된 카드 인덱스입니다.");
                return;
        }

        // 선택된 리스트에서 활성화된 카드들만 필터링하여 리스트 생성
        List<GameObject> activeCards = selectedList.FindAll(card => card.activeSelf);

        if (activeCards.Count > 0)
        {
            // 활성화된 카드가 있다면, 그 중 하나를 무작위로 선택하여 비활성화
            int randomIndex = Random.Range(0, activeCards.Count);
            activeCards[randomIndex].SetActive(false);

            // 사용한 카드를 drawnCards에서 제거하지 않음으로써 이후에 다시 드로우될 수 있도록 설정
            Debug.Log($"카드 {card_index} 리스트에서 랜덤으로 카드 {randomIndex + 1}을(를) 비활성화하고 다시 덱에 추가했습니다.");
        }
        else
        {
            Debug.Log($"카드 {card_index} 리스트에 활성화된 카드가 없습니다.");
        }
    }
    public override void EndAdventure()
    {

        GrantBaseResources();
        owngold = randomresource(baseresource);
        owntungsten = randomresource(baseresource);
        if (owngold)
        {
            resourceManager.AddResource("금", 0, 1);
        }
        if (owntungsten)
        {
            resourceManager.AddResource("텅스텐", 0, 1);
        }
        Playeradventureendobject.SetActive(true);
        ownironText.text = "얻은 철 갯수:" + baseIron;
        ownwoodText.text = "얻은 나무 갯수:" + baseWood;
        ownironswordText.text = "얻은 철 검 갯수" + baseironsword;
        if (owngold)
        {
            owngoldText.text = "금 획득 성공!";
        }
        else
        {
            owngoldText.text = "금 획득 실패!";
        }
        if (owntungsten)
        {
            owntungstenText.text = "텅스텐 획득 성공!";
        }
        else
        {
            owntungstenText.text = "텅스텐 획득 실패!";
        }


    }
    public void GomainScene()
    {
        SceneManager.LoadScene("Main");

        questSettingManager = QuestSettingManager.instance;
        //참조 실패 하도 많이 떠서 두개의 방법으로 찾습니다. 싱글톤으로 먼저 찾되, 없으면<null 일시> findobjectType으로 행동합니다.
        playerManager = PlayerManager.instance ?? FindObjectOfType<PlayerManager>();
        inven = invenmanager.instance ?? FindObjectOfType<invenmanager>();
        resourceManager = ResourceManager.instance ?? FindObjectOfType<ResourceManager>();

        if (playerManager != null && inven != null && resourceManager != null)
        {
            playerManager.FindUimanager();
            inven.FindUimanager();
            resourceManager.FindUimanager();
            inven.IncreaseItemCount_in_stringint("철 검", baseironsword); // 철 검 1개 추가
        }
        else
        {
            Debug.LogError("씬 전환 후 필요한 매니저가 null입니다. 연결을 확인하세요.");
        }
        if(questSettingManager != null)
        {
            questSettingManager.LevelUp_Quest_open();
        }
    }
}



# --- File: Assets\Script\MonoBehavior\explansupport.cs ---
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using UnityEngine;

public class explansupport : MonoBehaviour
{

    [SerializeField]private List<GameObject> Gameexp;  // 이미지 리스트
    [SerializeField] private int nowexp = 0;  // 현재 활성화된 이미지의 인덱스
    [SerializeField] private GameObject nextbutton;
    [SerializeField] private GameObject backbutton;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
    }

    // 클릭된 버튼에 해당하는 이미지를 활성화하고 나머지는 비활성화
    private void imageController(int index)
    {
        // 리스트의 모든 이미지를 비활성화
        foreach (GameObject gameObject in Gameexp)
        {
            gameObject.SetActive(false);
        }

        // 선택된 인덱스의 이미지만 활성화
        if (index >= 0 && index < Gameexp.Count)  // 유효한 인덱스인지 확인
        {
            Gameexp[index].gameObject.SetActive(true);
        }

    }
    public void nextbuttonclick()
    {
        nowexp = nowexp + 1;
        imageController(nowexp);
        
        if(nowexp >= 1)
        {
            backbutton.SetActive(true);
        }
        if(nowexp == 4) 
        {
            nextbutton.SetActive(false);
        }
    }
    public void backbuttonclick()
    {
        nowexp = nowexp - 1;
        imageController(nowexp);
        
        if (nowexp == 0)
        {
            backbutton.SetActive(false);
        }
        if (nowexp <= 3)
        {
            nextbutton.SetActive(true);
        }
    }
}


# --- File: Assets\Script\MonoBehavior\forgedscript.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class forgedscript : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}


# --- File: Assets\Script\MonoBehavior\Gamemanager.cs ---
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
#if UNITY_EDITOR
using UnityEditor;
using static UnityEditor.Progress;
#endif
using UnityEngine;
using TMPro;
using UnityEngine.UI;
public class GameManager : MonoBehaviour
{
    [SerializeField] private Sprite item_sprite;
    [SerializeField] private Image item_image;
    [SerializeField] private TextMeshProUGUI item_name;
    public Itemdata itemdata;

    public string Weaponname;

    private PlayerManager playerManager;

    public TextMeshProUGUI item1SuccessRateText; 
    private void Awake()
    {
        itemname();
    }

    private void Update()
    {
        Successprobabilitytext();

        
        
    }
    private void Start()
    {
        playerManager = PlayerManager.instance;
        item_sprite = itemdata.sprite;
        if (item_image != null && item_sprite != null)
        {
            item_image.sprite = item_sprite;
        }
        if(item_name != null)
        {
            item_name.text = Weaponname;
        }
        if (playerManager == null)
        {
            Debug.LogError("PlayerManager를 찾을 수 없습니다.");
        }
    }
    // 강화 버튼 onclick

    public void ClickMadeButton()
    {
        if (Weaponname != null)
        {
            playerManager.MadeWeapon(itemdata);
            Debug.Log(itemdata + " 제작 완료!");
        }
        else
        {
            Debug.LogError("Weaponname이 null입니다!!");
        }
        Soundmanager.instance.PlayHammersound();
    }
    private void itemname()
    {
        Weaponname = itemdata.itemname;
    }
    private void Successprobabilitytext()
    {
        playerManager.ShowWeaponSuccessRate(itemdata, item1SuccessRateText);
    }
    
}



# --- File: Assets\Script\MonoBehavior\Gameobjectmanager.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Gameobjectmanager : MonoBehaviour
{
    private PlayerManager playerManager;
    private PlayerGuildManager playerGuildManager;
    private UIManager uiManager;
    private ResourceManager resourceManager;
    public QuestSettingManager questSettingManager;

    public int playerwantlevel = 1;
    public invenmanager inven;
    public GameObject uiobjects;
    public GameObject nonuiobjects;
    public GameObject bagobject; // ���� ������Ʈ
    public GameObject noiron; // ���� ��ᰡ ���� �� ��� ��.
    public GameObject fail_made;
    public GameObject PaperObject;
    // Start is called before the first frame update

    [SerializeField] private List<GameObject> non_open_ui;
    private void Start()
    {
        playerManager = PlayerManager.instance;
        resourceManager = ResourceManager.instance;
        uiManager = UIManager.instance;
        questSettingManager = QuestSettingManager.instance;
    }
    private void Update()
    {

    }
    public void Level_limited_OnUi()
    {
        if (PlayerManager.instance.PlayerLevelCheck(playerwantlevel))
        {
            uiobjects.SetActive(true);
        }
        else
        {
            nonuiobjects.SetActive(true);
        }
    }
    public void Onui()
    {
        uiobjects.SetActive(true);
    }
    public void Offui()
    {
        uiobjects.SetActive(false);

    }
    public void GoMainScene()
    {
        SceneManager.LoadScene("main");
        //uiManager.UpdateAllUI();
        if (questSettingManager != null)
        {
            questSettingManager.LevelUp_Quest_open();
        }
    }
    public void adventurescene()
    {
        bool adventureticket = ResourceManager.instance.UseResource("탐험 허가증", 1);
        if (adventureticket)
        {
            SceneManager.LoadScene("adventure_scene");
        }
        else
        {
            Debug.Log("Ž�� �㰡���� �����ϴ�.");
        }
        
    }
    public void failed_made_noiron()
    {
        noiron.SetActive(false);
    }
    public void paper_object_on()
    {
        PaperObject.SetActive(true);
        Soundmanager.instance.PlayPapersound();
    }
    public void paper_object_off()
    {
        PaperObject.SetActive(false);
        Soundmanager.instance.PlayPapersound();
    }
    public void failedmadeweapon_failed()
    {
        fail_made.SetActive(false);
    }
    public void open_bag()
    {
        bagobject.SetActive(true);
        Debug.Log("���� ����");
    }
    public void close_bag()
    {
        bagobject.SetActive(false);
        Debug.Log("���� ����");
    }
    public void open_questobject()
    {
        uiobjects.SetActive(true);
        if(questSettingManager != null)
        {
            questSettingManager.LevelUp_Quest_open();
        }
        else
        {
            Debug.LogError("����Ʈ �Ŵ��� ����!! ���̴�!! ���!!!");
        }
    }
    public void protected_ui_open()
    {
        bool isAnyNonOpenUIActive = false;

        // non_open_ui ����Ʈ�� ��ȸ�ϸ� �ϳ��� Ȱ��ȭ�Ǿ� �ִ��� Ȯ��
        foreach (GameObject ui in non_open_ui)
        {
            if (ui != null && ui.activeSelf)
            {
                isAnyNonOpenUIActive = true;
                break; // �ϳ��� Ȱ��ȭ�Ǿ� ������ �� �̻� Ȯ���� �ʿ� ����
            }
        }

        // ���ǿ� ���� uiobjects�� Ȱ��ȭ ���� ����
        if (isAnyNonOpenUIActive)
        {
            uiobjects.SetActive(false); // non_open_ui �� �ϳ��� Ȱ��ȭ�Ǿ� ������ uiobjects ��Ȱ��ȭ
            Debug.Log("non_open_ui�� Ȱ��ȭ�� UI�� �־� uiobjects�� ��Ȱ��ȭ�߽��ϴ�.");
        }
        else
        {
            uiobjects.SetActive(true); // ��� ��Ȱ��ȭ�Ǿ� ������ uiobjects Ȱ��ȭ
            Debug.Log("non_open_ui�� Ȱ��ȭ�� UI�� �����Ƿ� uiobjects�� Ȱ��ȭ�߽��ϴ�.");
        }
    }
    public void protected_bag_open()
    {
        bool isAnyNonOpenUIActive = false;

        // non_open_ui ����Ʈ�� ��ȸ�ϸ� �ϳ��� Ȱ��ȭ�Ǿ� �ִ��� Ȯ��
        foreach (GameObject ui in non_open_ui)
        {
            if (ui != null && ui.activeSelf)
            {
                isAnyNonOpenUIActive = true;
                break; // �ϳ��� Ȱ��ȭ�Ǿ� ������ �� �̻� Ȯ���� �ʿ� ����
            }
        }

        // ���ǿ� ���� uiobjects�� Ȱ��ȭ ���� ����
        if (isAnyNonOpenUIActive)
        {
            bagobject.SetActive(false); // non_open_ui �� �ϳ��� Ȱ��ȭ�Ǿ� ������ uiobjects ��Ȱ��ȭ
            Debug.Log("non_open_ui�� Ȱ��ȭ�� UI�� �־� uiobjects�� ��Ȱ��ȭ�߽��ϴ�.");
        }
        else
        {
            bagobject.SetActive(true); // ��� ��Ȱ��ȭ�Ǿ� ������ uiobjects Ȱ��ȭ
            Debug.Log("non_open_ui�� Ȱ��ȭ�� UI�� �����Ƿ� uiobjects�� Ȱ��ȭ�߽��ϴ�.");
        }
    }
    public void protected_paper_open()
    {
        bool isAnyNonOpenUIActive = false;

        // non_open_ui ����Ʈ�� ��ȸ�ϸ� �ϳ��� Ȱ��ȭ�Ǿ� �ִ��� Ȯ��
        foreach (GameObject ui in non_open_ui)
        {
            if (ui != null && ui.activeSelf)
            {
                isAnyNonOpenUIActive = true;
                break; // �ϳ��� Ȱ��ȭ�Ǿ� ������ �� �̻� Ȯ���� �ʿ� ����
            }
        }

        // ���ǿ� ���� uiobjects�� Ȱ��ȭ ���� ����
        if (isAnyNonOpenUIActive)
        {
            PaperObject.SetActive(false); // non_open_ui �� �ϳ��� Ȱ��ȭ�Ǿ� ������ uiobjects ��Ȱ��ȭ
            Debug.Log("non_open_ui�� Ȱ��ȭ�� UI�� �־� uiobjects�� ��Ȱ��ȭ�߽��ϴ�.");
        }
        else
        {
            PaperObject.SetActive(true); // ��� ��Ȱ��ȭ�Ǿ� ������ uiobjects Ȱ��ȭ\
            Soundmanager.instance.PlayPapersound();
            Debug.Log("non_open_ui�� Ȱ��ȭ�� UI�� �����Ƿ� uiobjects�� Ȱ��ȭ�߽��ϴ�.");
        }
    }
}


# --- File: Assets\Script\MonoBehavior\invenmanager.cs ---
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class invenmanager : MonoBehaviour
{
    public static invenmanager instance;
    public PlayerManager PlayerManager;
    private UIManager uimanager;


    // Start is called before the first frame update
    //철검 제작 횟수 증가 및 텍스트 업데이트 함수까지 호출해주는 함수

    public Dictionary<string, int> itemCounts = new Dictionary<string, int>();
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
        DictionaryUpdate();
        uimanager = UIManager.instance;
    }
    public void FindUimanager()
    {
        uimanager = UIManager.instance;
    }
    private void Start()
    {
    
        if (uimanager != null)
        {
            uimanager.UpdatePlayerUI();
        }
        UpdateUI();
    }
    // Update is called once per frame
    private void Update()
    {
        FindUimanager();
    }

    public void IncreaseItemCount(Itemdata itemdata)
    {
        if (itemCounts.ContainsKey(itemdata.itemname))
        {
            itemCounts[itemdata.itemname] = itemCounts[itemdata.itemname] + 1;  
            UpdateUI();
        }
        else
        {
            Debug.LogError("잘못된 아이템 이름: " + itemdata.itemname);
        }
    }
    public void IncreaseItemCount_in_stringint(string itemName, int count)
    {
        if (itemCounts.ContainsKey(itemName))
        {
            itemCounts[itemName] += count;
            UpdateUI();
        }
        else
        {
            Debug.LogError("잘못된 아이템 이름: " + itemName);
        }
    }
    public void UpdateUI()
    {
        if (uimanager != null)
        {
            uimanager.UpdateInventoryUI();
        }
        else
        {
            uimanager = FindObjectOfType<UIManager>();
        }
    }

    public void DictionaryUpdate()
    {
        itemCounts["철 검"] = 0;
        itemCounts["나무 검"] = 0;
        itemCounts["철 갑옷"] = 0;
        itemCounts["철 괭이"] = 0;
        itemCounts["철 방패"] = 0;
        itemCounts["철 창"] = 0;
        itemCounts["철 검 묶음"] = 0;
        itemCounts["은 목걸이"] = 0;
        itemCounts["강철 검"] = 0;
        itemCounts["금 목걸이"] = 0;
        itemCounts["금 갑옷"] = 0;
        itemCounts["마검 - 사라트"] = 0;
        itemCounts["마검 - 삼위일체"] = 0;
        itemCounts["마검 - 알 반살"] = 0;
        itemCounts["마검 - 본다르"] = 0;
    }
    public void UpdateAllUIText()
    {
        foreach (KeyValuePair<string, int> item in itemCounts)
        {
            UpdateUI();
        }
    }
    //불러오기 후 변수와 딕셔너리 동기화
    public void LoadDataAndSync()
    {
        UpdateUI();
    }



}


# --- File: Assets\Script\MonoBehavior\PlayerManager.cs ---
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
    public string UserID;
    public int gold = 1500;
    public int morality = 50;
    public int Playerlevel = 1;
    public int score = 0;

    public float bgmVolume = 1f; // 브금 볼륨 (0~1)

    public int requiredGold = 0;
    public int requiredReputation = 0;
    public List<int> hammer_have;    
    

    Resource resource;
    [SerializeField]
    private QuestSettingManager questSettingManager;

    public hammerdata hammerdata;
    public invenmanager invenmanager;


    public ScoreDisplay scoreDisplay; // ScoreDisplay 컴포넌트 참조

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
        NetworkManager.Instance.Initialize();

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
                int scoreIncrease = 50; // 증가시킬 점수량 정의

                string myUserId = this.UserID; // 로그인한 유저 ID
                NetworkManager.Instance.SendScoreAdd(myUserId, 150);


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


# --- File: Assets\Script\MonoBehavior\ResourceManager.cs ---
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

// 앞으로 자원 등은 다 여기서 관리 할거임 다른 스크립트 만들지 말고 새로운 자원 추가하면 Mineral부터 뒤져보도록 하자
public class ResourceManager : MonoBehaviour
{
    public static ResourceManager instance;
    public Dictionary<string, Resource> resources = new Dictionary<string, Resource>();
    
    private UIManager uimanager;


    public PlayerManager playerManager;
    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
        InitializeResources();
        uimanager = FindObjectOfType<UIManager>();
    }
    public void FindUimanager()
    {
        uimanager = FindObjectOfType<UIManager>();
    }
    private void Start()
    {
        

        if (uimanager != null)
        {
            uimanager.UpdatePlayerUI();
        }
        // "Player" 게임 오브젝트를 찾음
        playerManager = PlayerManager.instance;

        // null이면 디버그 처리
        if (playerManager == null)
        {
            Debug.LogError("PlayerManager를 찾을 수 없습니다.");
        }
    }
    private void Update()
    {
        resourcestext();
    }
    private void InitializeResources()
    {
        AddResource("철", 100, 0);
        AddResource("나무", 50, 0);
        AddResource("금", 100, 0);
        AddResource("텅스텐", 0, 0);
        AddResource("탐험 허가증", 1000, 0);
    }

    // 자원 추가 함수
    public void AddResource(string resourceName, int price, int amount)
    {
        if (resources.ContainsKey(resourceName))
        {
            resources[resourceName].AddResource_in_resourceclass(amount);
        }
        else
        {
            resources.Add(resourceName, new Resource(resourceName, price, amount));
        }
    }
    //json파일 불러오기용 setresource 함수이다.
    public void SetResource(string resourceName, int amount)
    {
        if (resources.ContainsKey(resourceName))
        {
            resources[resourceName].quantity = amount;
        }
        else
        {
            resources.Add(resourceName, new Resource(resourceName, 0, amount));
        }
    }
    //자원 소모 함수이다. 만약 플레이어가 해당 자원을 이거 이상으로 보유하지 못했을 시 false를 반환하여 플레이어의 자원 사용을 막아버린다.
    public bool UseResource(string resourceName, int amount)
    {
        if (resources.ContainsKey(resourceName))
        {
            return resources[resourceName].UseResource(amount);
        }
        Debug.LogWarning($"{resourceName} 자원이 없습니다.");
        return false;
    }
    // 자원 양 조회 함수
    public int GetResourceAmount(string resourceName)
    {
        if (resources.ContainsKey(resourceName))
        {
            return resources[resourceName].quantity;
            
        }
        else
        {
            Debug.Log("그런 자원 없습니다.");
            return 0;
        }
    }


    private void resourcestext()
    {
        if(uimanager != null)
        {
            uimanager.UpdateResourceUI();
        }
        
    }

    
}

public class Resource
{
    public string name;   // 자원의 이름
    public int price;     // 자원의 가격
    public int quantity;  // 플레이어가 보유한 자원의 양

    // 생성자: 자원의 이름, 가격, 보유량을 초기화
    public Resource(string name, int price, int quantity)
    {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }

    // 자원 추가 함수
    public void AddResource_in_resourceclass(int amount)
    {
        quantity += amount;
    }

    // 자원 소모 함수
    public bool UseResource(int amount)
    {
        if (quantity >= amount)
        {
            quantity -= amount;
            return true;
        }
        return false; // 자원이 부족할 경우 false 반환
    }
}

# --- File: Assets\Script\MonoBehavior\SettingScript.cs ---
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class SettingScript : MonoBehaviour
{
    public AudioSource audioSource; // 오디오 소스를 드래그로 연결
    public Slider volumeSlider; // Slider UI를 드래그로 연결

    private PlayerManager playerManager;
    private invenmanager inven;
    private ResourceManager resourceManager;

    [SerializeField] private TextMeshProUGUI volumeText;

    private const string VolumeKey = "Volume"; // PlayerPrefs 키값

    void Awake()
    {
        // 게임 시작 시 저장된 값 불러오기
        float savedVolume = PlayerPrefs.GetFloat(VolumeKey, 100f); // 저장된 볼륨 값, 없으면 기본값 100
        ApplyVolume(savedVolume);
    }

    void Start()
    {
        playerManager = PlayerManager.instance;
        inven = invenmanager.instance;
        resourceManager = ResourceManager.instance;
        // 슬라이더 초기값 설정
        if (volumeSlider != null)
        {
            volumeSlider.value = PlayerPrefs.GetFloat(VolumeKey, 100f); // 저장된 값을 슬라이더에 반영
            volumeSlider.onValueChanged.AddListener(OnVolumeChanged); // 슬라이더 값 변경 이벤트
        }
    }

    public void OnVolumeChanged(float sliderValue)
    {
        // 슬라이더 값 변경 시 볼륨 적용
        ApplyVolume(sliderValue);

        // PlayerPrefs에 볼륨 값 저장
        PlayerPrefs.SetFloat(VolumeKey, sliderValue);
        PlayerPrefs.Save();
    }

    private void ApplyVolume(float volume)
    {
        if (audioSource != null)
        {
            // Slider 값 (0~100)을 AudioSource.volume 값 (0~1)로 변환
            audioSource.volume = volume / 100f;
        }

        // 볼륨 텍스트 업데이트
        UpdateVolumeText(volume);
    }
    public void MasterID_For_Professor()
    {
        playerManager.gold = 10000000;
        playerManager.Playerlevel = 10;
        playerManager.AddResources_in_Player(500, 500, 500, 500);
        ResourceManager.instance.AddResource("탐험 허가증", 1000, 20);
    }
    private void UpdateVolumeText(float volume)
    {
        if (volumeText != null)
        {
            int volumeInt = Mathf.RoundToInt(volume); // 소수점 제거
            volumeText.text = $"{volumeInt}";
        }
    }

    public void QuitGame()
    {
        #if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
        #else
        Application.Quit();
        #endif

        Debug.Log("게임 종료");
    }
}


# --- File: Assets\Script\MonoBehavior\Soundmanager.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Soundmanager : MonoBehaviour
{
    public static Soundmanager instance { get; set; }
    [SerializeField]
    private AudioSource hammerSource;
    [SerializeField]
    private AudioSource GoldSource;
    [SerializeField]
    private AudioSource PaperSource;
    [SerializeField]
    private AudioSource hitstoneSource;
    [SerializeField]
    private AudioSource breakstoneSource;
    [SerializeField]
    private AudioSource hitwoodSource;
    [SerializeField]
    private AudioSource breakwoodSource;
    [SerializeField]
    private AudioClip hammersound;
    [SerializeField]
    private AudioClip hitstonesound;
    [SerializeField]
    private AudioClip breakstonesound;
    [SerializeField]
    private AudioClip Goldsound;
    [SerializeField]
    private AudioClip Papersound;
    [SerializeField]
    private AudioClip hitwoodsound;
    [SerializeField]
    private AudioClip breakwoodsound;
    // Start is called before the first frame update
    private void Awake()
    {
        if(instance == null)
        {
            instance = this;
        }
        else
        {
            Destroy(gameObject);
        }

    }
    private void Start()
    {
        
    }
    // Update is called once per frame
    private void Update()
    {

    }
    public void PlayHammersound()
    {
        hammerSource.clip = hammersound;
        hammerSource.Play();
    }
    public void PlayPapersound()
    {
        PaperSource.clip = Papersound;
        PaperSource.Play();
    }
    public void PlayGoldsound()
    {
        GoldSource.clip = Goldsound;
        GoldSource.Play();
    }
    public void Playhitstonesound()
    {
        hitstoneSource.clip = hitstonesound;
        hitstoneSource.Play();
    }
    public void Playbreakstonesound()
    {
        breakstoneSource.clip = breakstonesound;
        breakstoneSource.Play();
    }
    public void Playhitwoodsound()
    {
        hitwoodSource.clip = hitwoodsound;
        hitwoodSource.Play();
    }
    public void Playbreakwoodsound()
    {
        breakwoodSource.clip = breakwoodsound;
        breakwoodSource.Play();
    }
}


# --- File: Assets\Script\MonoBehavior\UiManager.cs ---
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




# --- File: Assets\Script\MonoBehavior\ending\angel_ending_controller.cs ---
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


# --- File: Assets\Script\MonoBehavior\ending\evill_ending_controller1.cs ---
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


# --- File: Assets\Script\MonoBehavior\hammer\Hammer_Index_Controler.cs ---
using System.Collections;
using System.Collections.Generic;
using JetBrains.Annotations;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;

public class Hammer_imformation : MonoBehaviour
{
    private PlayerManager playerManager;
    [SerializeField] private GameObject Hammer_index_prefab;
    [SerializeField] private int hammerindex;
    [SerializeField] private hammerdata hammerdata;
    [SerializeField] private Button equipbutton;
    [SerializeField] private Button buybutton;
    [SerializeField] private Button usedbutton;
    [SerializeField] private Image prefab_hammer_sprite;

    [SerializeField] private TextMeshProUGUI prefab_hammer_successrate;
    [SerializeField] private TextMeshProUGUI prefab_hammer_price;
    [SerializeField] private TextMeshProUGUI prefab_hammer_name;

    [SerializeField] private GameObject lack_gold;



    // Start is called before the first frame update
    void Start()
    {
        playerManager = PlayerManager.instance;
        PrefabUi();
        Check_have_hammer();

    }

    // Update is called once per frame
    void Update()
    {
        
    }
    private void PrefabUi()
    {
        if (prefab_hammer_price != null)
        {
            prefab_hammer_price.text = $"망치 가격 : {hammerdata.hammer_price}";
        }
        if (prefab_hammer_successrate != null)
        {
            prefab_hammer_successrate.text = $"추가 강화 성공 확률 : {hammerdata.hammer_base_successRate}";
        }
        if(prefab_hammer_name != null)
        {
            prefab_hammer_name.text = hammerdata.hammer_name;
        }
        if(prefab_hammer_sprite != null)
        {
            prefab_hammer_sprite.sprite = hammerdata.sprite;
        }
    }
    public void DestroyPrefab()
    {
        if (Hammer_index_prefab != null)
        {
            Destroy(Hammer_index_prefab); // questPrefab을 삭제
            Debug.Log("Hammer_index_prefab이 삭제되었습니다.");
        }
        else
        {
            Debug.LogWarning("Hammer_index_prefab이 할당되지 않았습니다.");
        }
    }
    private void Check_have_hammer()
    {
        int hammerState = playerManager.hammer_have[hammerindex];
        Debug.Log($"hammerindex: {hammerindex}, hammerState: {hammerState}");
        switch (hammerState)
        {
            case 0:
                buybutton.gameObject.SetActive(true);
                equipbutton.gameObject.SetActive(false);
                usedbutton.gameObject.SetActive(false);
                Debug.Log("case 0: 발동 (구매 가능)");
                break;

            case 1:
                equipbutton.gameObject.SetActive(true);
                buybutton.gameObject.SetActive(false);
                usedbutton.gameObject.SetActive(false);
                Debug.Log("case 1: 발동 (장착 가능)");
                break;

            case 2:
                usedbutton.gameObject.SetActive(true);
                equipbutton.gameObject.SetActive(false);
                buybutton.gameObject.SetActive(false);
                Debug.Log("case 2: 발동 (사용 중)");
                break;

            default:
                Debug.LogWarning("Invalid hammer state!");
                break;
        }
    }
    public void Onclick_buybutton()
    {
        if(playerManager.gold >= hammerdata.hammer_price)
        {
            playerManager.gold = playerManager.gold - hammerdata.hammer_price;
            playerManager.hammer_have[hammerindex] = 1;
            Check_have_hammer();
        }
        else
        {
            lack_gold.gameObject.SetActive(true);
        }
    }
    public void Onclick_equipbutton()
    {
        if (playerManager.hammerdata !=  hammerdata)
        {
            for (int i = 0; i < playerManager.hammer_have.Count; i++)
            {
                if (playerManager.hammer_have[i] == 2) // 이전에 사용 중(2) 상태인 망치를 찾음
                {
                    playerManager.hammer_have[i] = 1; // 상태를 1로 변경 (장착 가능 상태)
                    Debug.Log($"이전 장착 망치 {i} 상태를 1로 변경했습니다.");
                    break;
                }
            }
            playerManager.hammer_have[hammerindex] = 2;
            playerManager.CurrentHammerData = hammerdata;
            Check_have_hammer();
        }
    }
    
}


# --- File: Assets\Script\MonoBehavior\hammer\ScriptableObjectController.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScriptableObjectController : MonoBehaviour
{
    public PlayerManager playerManager;

    // 교체할 ScriptableObject
    public List<hammerdata> hammerOptions;


    // Start is called before the first frame update
    void Start()
    {
        playerManager = PlayerManager.instance;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void SelectHammer(int hammerIndex)
    {
        if (hammerIndex >= 0 && hammerIndex < hammerOptions.Count)
        {
            playerManager.CurrentHammerData = hammerOptions[hammerIndex];
            Debug.Log($"Selected hammer: {hammerOptions[hammerIndex].hammer_name}");
        }
        else
        {
            Debug.LogError("Invalid hammer index selected!");
        }
    }
}


# --- File: Assets\Script\MonoBehavior\Quest\PlayerGuildManager.cs ---
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


# --- File: Assets\Script\MonoBehavior\Quest\PrefabController.cs ---
using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using static System.Net.Mime.MediaTypeNames;

public class PrefabController : PlayerGuildManager
{
    [SerializeField] private GameObject questPrefab;
    [SerializeField] private TextMeshProUGUI want_text_one;
    [SerializeField] private TextMeshProUGUI want_text_two;
    [SerializeField] private TextMeshProUGUI want_text_three;
    [SerializeField] private TextMeshProUGUI reward;
    [SerializeField] private int Quest_index = 1;

    // 생성된 Prefab을 저장할 변수
    private GameObject currentQuest;

    // 버튼 클릭 시 호출될 메소드

    // Start is called before the first frame update
    private void Awake()
    {
        findObject();
        settingtext_by_Game();
    }
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void ShowQuest()
    {
        if (currentQuest == null) // Quest가 이미 화면에 나타나지 않았을 때만 생성
        {
            // Quest 1 Prefab을 main_Canvas의 자식으로 생성
            currentQuest = Instantiate(questPrefab, new Vector3(0, 0, 0), Quaternion.identity);

            // main_Canvas 찾기
            Transform canvasTransform = GameObject.Find("main_Canvas").transform;

            if (canvasTransform != null)
            {
                // 생성된 Prefab을 main_Canvas의 자식으로 설정
                currentQuest.transform.SetParent(canvasTransform, false);

                Debug.Log("Prefab 생성 완료!");
                Soundmanager.instance.PlayPapersound();
            }
            else
            {
                Debug.LogWarning("main_Canvas를 찾을 수 없습니다.");
            }
        }
    }
    public void Clickquestbutton()
    {
        QuestPotal(Quest_index);
        UIupdate();

    }
    private void UIupdate()
    {
        settingtext_by_Game();
        Debug.Log("Uidate가 발동함");
    }
    public void DestroyQuestPrefab()
    {
        if (questPrefab != null)
        {
            Destroy(questPrefab); // questPrefab을 삭제
            Debug.Log("QuestPrefab이 삭제되었습니다.");
            Soundmanager.instance.PlayPapersound();
        }
        else
        {
            Debug.LogWarning("questPrefab이 할당되지 않았습니다.");
        }
    }
    void findObject()
    {
        playerManager = PlayerManager.instance;
        inven = invenmanager.instance;
    }
    private void settingtext_by_Game()
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
        // questtext_list가 null이 아니고 크기가 1 이상인지 확인
        if (questtext_list != null && questtext_list.Count > 0)
        {
            // Quest_index가 1 이상이고 questtext_list의 크기 이내인지를 체크
            if (Quest_index > 0 && Quest_index <= questtext_list.Count)
            {
                int Questarr = Quest_index - 1;
                switch (Quest_index)
                {
                    case 1:
                        want_text_one.text = $"보유 철 검 : {inven.itemCounts["철 검"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;

                    case 2:
                        want_text_one.text = $"보유 철 검 : {inven.itemCounts["철 검"]}";
                        want_text_two.text = $"보유 철 갑옷 : {inven.itemCounts["철 갑옷"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;

                    case 3:
                        want_text_one.text = $"보유 철 검 : {inven.itemCounts["철 검"]}";
                        want_text_two.text = $"보유 철 갑옷 : {inven.itemCounts["철 갑옷"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 4:
                        want_text_one.text = $"보유 부러진 검 : {playerManager.brokenSword}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 5:
                        want_text_one.text = $"보유 나무 검 : {inven.itemCounts["나무 검"]}";
                        want_text_two.text = $"보유 철 괭이 : {inven.itemCounts["철 괭이"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 6:
                        want_text_one.text = $"보유 철 검 : {inven.itemCounts["철 검"]}";
                        want_text_two.text = $"보유 철 창 : {inven.itemCounts["철 창"]}";
                        want_text_three.text = $"보유 철 방패 : {inven.itemCounts["철 방패"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 7:
                        want_text_one.text = $"보유 철 검 : {inven.itemCounts["철 검"]}";
                        want_text_two.text = $"보유 철 창 : {inven.itemCounts["철 창"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 8:
                        want_text_one.text = $"보유 강철 검 : {inven.itemCounts["강철 검"]}";
                        want_text_two.text = $"보유 철 검 묶음 : {inven.itemCounts["철 검 묶음"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 9:
                        want_text_one.text = $"보유 강철 검 : {inven.itemCounts["강철 검"]}";
                        want_text_two.text = $"보유 철 갑옷 : {inven.itemCounts["철 갑옷"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 10:
                        want_text_one.text = $"보유 강철 검 : {inven.itemCounts["강철 검"]}";
                        want_text_two.text = $"보유 은 목걸이 : {inven.itemCounts["은 목걸이"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 11:
                        want_text_one.text = $"보유 강철 검 : {inven.itemCounts["강철 검"]}";
                        want_text_two.text = $"보유 은 목걸이 : {inven.itemCounts["은 목걸이"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 12:
                        want_text_one.text = $"보유 금 갑옷 : {inven.itemCounts["금 갑옷"]}";
                        want_text_two.text = $"보유 금 목걸이 : {inven.itemCounts["금 목걸이"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 13:
                        want_text_one.text = $"보유 강철 검 : {inven.itemCounts["강철 검"]}";
                        want_text_two.text = $"보유 금 목걸이 : {inven.itemCounts["금 목걸이"]}";
                        want_text_three.text = $"보유 마검-사라트 : {inven.itemCounts["마검 - 사라트"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 14:
                        want_text_one.text = $"보유 금 갑옷 : {inven.itemCounts["금 갑옷"]}";
                        want_text_two.text = $"보유 금 목걸이 : {inven.itemCounts["금 목걸이"]}";
                        want_text_three.text = $"보유 철 방패 : {inven.itemCounts["철 방패"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 15:
                        want_text_one.text = $"마검 - 사라트 : {inven.itemCounts["마검 - 사라트"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 16:
                        want_text_one.text = $"마검 - 삼위일체 : {inven.itemCounts["마검 - 삼위일체"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    case 17:
                        want_text_one.text = $"마검 - 본다르 : {inven.itemCounts["마검 - 본다르"]}";
                        reward.text = questtext_list[Questarr];  // 정상적으로 questtext_list에서 값을 가져옵니다.
                        break;
                    // 추가적인 case를 여기에 삽입하여 다양한 퀘스트를 처리할 수 있습니다.
                    default:
                        Debug.Log("존재하지 않는 Quest_index입니다.");
                        break;
                }
            }
            else
            {
                Debug.LogError("Quest_index가 questtext_list 범위를 벗어났습니다.");
            }
        }
        else
        {
            Debug.LogError("questtext_list가 초기화되지 않았거나 비어 있습니다.");
        }

    }

}


# --- File: Assets\Script\MonoBehavior\Quest\PrefabOpen.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

public class PrefabOpen : MonoBehaviour
{
    [SerializeField] private GameObject questPrefab;
    private GameObject currentQuest;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void ShowQuest()
    {
        if (currentQuest == null) // Quest가 이미 화면에 나타나지 않았을 때만 생성
        {
            // Quest 1 Prefab을 main_Canvas의 자식으로 생성
            currentQuest = Instantiate(questPrefab, new Vector3(0, 0, 0), Quaternion.identity);

            // main_Canvas 찾기
            Transform canvasTransform = GameObject.Find("main_Canvas").transform;

            if (canvasTransform != null)
            {
                // 생성된 Prefab을 main_Canvas의 자식으로 설정
                currentQuest.transform.SetParent(canvasTransform, false);

                Debug.Log("Prefab 생성 완료!");
                Soundmanager.instance.PlayPapersound();
            }
            else
            {
                Debug.LogWarning("main_Canvas를 찾을 수 없습니다.");
            }
        }
    }
}


# --- File: Assets\Script\MonoBehavior\Quest\QuestSettingManager.cs ---
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


# --- File: Assets\Script\Savemanager\DataManager.cs ---
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class DataManager : MonoBehaviour
{
    public PlayerManager playerManager;
    public ResourceManager resourcemanager;
    public invenmanager inven;
    public QuestSettingManager questSettingManager;


    [SerializeField] private List<hammerdata> hammerDatas; //해머 데이터를 불러오기 위해 데이터 매니저에 일단 해머데이터를 연결시켜주기로 함.
    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject); // 씬이 바뀌어도 유지
        }
        else
        {
            Destroy(gameObject);
        }

        filePath = Path.Combine(Application.persistentDataPath, "playerData.json");
    }
    // Start is called before the first frame update
    private void Start()
    {
        playerManager = PlayerManager.instance;
        resourcemanager = ResourceManager.instance;
        questSettingManager = QuestSettingManager.instance;
        inven = invenmanager.instance;

    }

    // Update is called once per frame
    private void Update()
    {
        
    }
    public static DataManager instance;
    private string filePath;
    public hammerdata GetHammerDataByName(string hammerName)
    {
        return hammerDatas.Find(hammer => hammer.hammer_name == hammerName);
    }
    //설명하자면 복잡하다. 일단,iron과 wood도 이제 리소스 매니저에있는 걸 긁어온다..

    //자원은 해봤자 4개 이내이기에 이정도가 편할 거라 생각해 이렇게 구현했다.
    //플레이어 데이터는 플레이어 데이터를 긁어온다. 원래도 개별 변수이고 개별 변수를 가져와서 다시 개별 변수로 입히기에 큰 설명이 필요없다.
    //인벤 데이터.. 이게 문젠데 딕셔너리를 통으로 가져오는 건 json 파일이 불가능하다고 한다. 그래서 리스트를 만들어서 딕셔너리를 리스트 형태로 저장해놓고
    //다시 돌아왔을 때 ( 로드 버튼을 눌렀을 떄) 리스트를 다시 딕셔너리로 변환하는 과정을 거친다.
    public void SaveData()
    {
        if (ResourceManager.instance == null)
        {
            Debug.LogError("ResourceManager가 없습니다. 저장할 수 없습니다.");
        }


        // PlayerData에 저장할 정보 세팅
        PlayerData data = new PlayerData(PlayerManager.instance, GameObject.FindObjectOfType<invenmanager>());

        // JSON으로 변환 후 파일로 저장
        string json = JsonUtility.ToJson(data, true);
        try
        {
            File.WriteAllText(Application.persistentDataPath + "/playerData.json", json);
            Debug.Log("데이터가 저장되었습니다.");
        }
        catch (Exception e)
        {
            Debug.LogError("데이터 저장에 실패했습니다: " + e.Message);
        }
        Debug.Log("데이터가 저장되었습니다.");
        Debug.Log(Application.persistentDataPath);
    }
    public void LoadData()
    {
        string path = Application.persistentDataPath + "/playerData.json";
        if (File.Exists(path))
        {
            resourcemanager = FindObjectOfType<ResourceManager>();
            // JSON 파일에서 데이터 읽기
            string json = File.ReadAllText(path);
            PlayerData data = JsonUtility.FromJson<PlayerData>(json);
            // 불러온 데이터를 PlayerManager에 적용
            if (PlayerManager.instance != null)
            {
                PlayerManager.instance.brokenSword = data.brokenSword;
                PlayerManager.instance.reputation = data.reputation;
                PlayerManager.instance.gold = data.gold;
                PlayerManager.instance.Playerlevel = data.playerLevel;
                PlayerManager.instance.morality = data.morality;
                PlayerManager.instance.hammer_have = new List<int>(data.hammer_have);

                // hammerdataName 복원
                if (!string.IsNullOrEmpty(data.hammerdataName))
                {
                    hammerdata selectedHammer = GetHammerDataByName(data.hammerdataName);
                    if (selectedHammer != null)
                    {
                        PlayerManager.instance.CurrentHammerData = selectedHammer;
                    }
                    else
                    {
                        Debug.LogError($"Hammer '{data.hammerdataName}'를 찾을 수 없습니다.");
                    }
                }

            }
            else
            {
                Debug.Log("PlayerManager.instance가 없음.");
            }
            playerManager.UpdatebrokenswordUI();
            playerManager.UpdateUI();
            // ResourceManager를 통한 자원 설정
            if (ResourceManager.instance != null)
            {
                ResourceManager.instance.resources.Clear(); // 기존 데이터 초기화
                foreach (ResourceData resource in data.resourceDatas)
                {
                    ResourceManager.instance.resources.Add(resource.Resourcename, new Resource(resource.Resourcename, resource.price, resource.count));
                }
                ResourceManager.instance.FindUimanager(); // UI 갱신
            }
            else
            {
                Debug.LogWarning("ResourceManager.instance가 없음.");
            }
            ResourceManager.instance.FindUimanager(); // UI 매니저 연결
            Debug.Log("ResourceManager 데이터가 복원되었습니다.");

            playerManager.UpdateUI();
            questSettingManager.LevelUp_Quest_open();


            // invenmanager에 카운트 데이터 적용
            invenmanager inven = PlayerManager.instance.invenmanager;
            if (inven != null)
            {
                inven.itemCounts.Clear(); // 기존 데이터를 초기화하고 불러온 데이터를 추가
                foreach (ItemCountData item in data.itemCounts)
                {
                    inven.itemCounts.Add(item.itemName, item.count);
                }
                inven.UpdateUI(); // UI 업데이트
            }
            else
            {
                Debug.Log("Invenmanager null");
            }

            Debug.Log("데이터가 로드되었습니다.");
        }
        else
        {
            Debug.LogWarning("저장된 데이터 파일이 없습니다.");
        }

    }

    // 데이터 저장 함수
    public void SavePlayerData(PlayerManager player, invenmanager inven)
    {
        PlayerData data = new PlayerData(player, inven);
        string json = JsonUtility.ToJson(data, true);
        File.WriteAllText(filePath, json);
        Debug.Log("플레이어 데이터 저장.");
    }
    // HammerDatabase 내부 클래스
    [System.Serializable]
    public class HammerDatabase
    {
        public List<hammerdata> hammerDatas; // 모든 hammerdata를 저장하는 리스트

        public hammerdata GetHammerByName(string name)
        {
            return hammerDatas.Find(h => h.hammer_name == name);
        }
    }

    public HammerDatabase hammerDatabase;

}


# --- File: Assets\Script\Savemanager\PlayerData.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[SerializeField]
public class PlayerData
{
    public List<ResourceData> resourceDatas;
    public int iron;
    public int wood;
    public int adventureTicket;
    public int brokenSword;
    public int reputation;
    public int gold;
    public int playerLevel;
    public int morality;

    public List<int> hammer_have; // hammer_have 리스트 추가
    public string hammerdataName; // hammerdata 이름 추가



    // invenmanager 관련 데이터 추가
    public List<ItemCountData> itemCounts;


    public PlayerData(PlayerManager player, invenmanager inven)
    {

        resourceDatas = new List<ResourceData>();
        if (ResourceManager.instance != null)
        {
            foreach (var resource in ResourceManager.instance.resources)
            {
                resourceDatas.Add(new ResourceData(resource.Value.name, resource.Value.price, resource.Value.quantity));
            }
        }

        brokenSword = player.brokenSword;
        reputation = player.reputation;
        gold = player.gold;
        playerLevel = player.Playerlevel;
        morality = player.morality;

        // hammer_have 리스트 저장
        hammer_have = new List<int>(player.hammer_have);
        // 현재 장착된 hammerdata 이름 저장
        hammerdataName = (player.hammerdata != null && !string.IsNullOrEmpty(player.hammerdata.hammer_name))
            ? player.hammerdata.hammer_name
            : "돌 망치";

        itemCounts = new List<ItemCountData>();
        foreach (KeyValuePair<string, int> item in inven.itemCounts)
        {
            itemCounts.Add(new ItemCountData(item.Key, item.Value));
        }

    }


}
//json 파일이 딕셔너리를 지원하지 않으므로. 새롭게 저장하기 위해 리스트를 사용했다. .. 하아...
[System.Serializable]
public class ItemCountData
{
    public string itemName;  // 아이템 이름
    public int count;        // 아이템 개수

    public ItemCountData(string itemName, int count)
    {
        this.itemName = itemName;
        this.count = count;
    }
}

[System.Serializable]
public class ResourceData
{
    public string Resourcename; // 자원의 이름
    public int price;           // 자원의 가격
    public int count;           // 자원의 개수

    public ResourceData(string resourcename, int price, int count)
    {
        Resourcename = resourcename;
        this.price = price;
        this.count = count;
    }
}

# --- File: Assets\Script\Savemanager\SelectSaveSlot.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using System.IO;

public class SelectSaveSlot : MonoBehaviour
{

}


# --- File: Assets\Script\Scriptableobjects\hammerdata.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "hammerdata", menuName = "hammerdata", order = 1)]
public class hammerdata : ScriptableObject
{
    public string hammer_name;
    public int hammer_base_successRate;
    public int hammer_price;
    public Sprite sprite;
    public int hammer_number;

}

# --- File: Assets\Script\Scriptableobjects\itemdata.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "itemdata", menuName = "itemdata", order = 1)]
public class Itemdata : ScriptableObject
{
    public string itemname;
    public int successRate;
    public int requiredIron;
    public int requiredWood;
    public int requiredGolds;
    public int requiredTungsten;
    public int item_count;
    public Sprite sprite;

}


# --- File: Assets\Script\Server\AccountRegisterUI.cs ---
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class AccountRegisterUI : MonoBehaviour
{
    [Header("Input Fields")]
    public TMP_InputField idInput;
    public TMP_InputField pwInput;

    [Header("Profile Selection")]
    public int currentSelectedIndex = 0; // 선택된 인덱스 (0~4)
    public Image[] profileSelectionHighlights; // 선택 표시용 테두리나 이미지 (옵션)

    // 프로필 버튼 클릭 시 호출 (Unity 인스펙터에서 0, 1, 2, 3, 4로 각각 할당)
    public void SetProfileIndex(int index)
    {
        currentSelectedIndex = index;

        // 시각적 강조 피드백
        for (int i = 0; i < profileSelectionHighlights.Length; i++)
        {
            profileSelectionHighlights[i].enabled = (i == index);
        }

        Debug.Log($"프로필 {index}번 선택됨");
    }

    // "회원가입 완료" 버튼 클릭 시 호출
    public void OnClickSubmitRegistration()
    {
        string id = idInput.text;
        string pw = pwInput.text;

        if (string.IsNullOrEmpty(id) || string.IsNullOrEmpty(pw))
        {
            Debug.LogWarning("아이디와 비밀번호를 모두 입력하세요.");
            return;
        }

        // NetworkManager를 통해 서버로 데이터 전송
        NetworkManager.Instance.SendCreateAccount(id, pw, currentSelectedIndex);

        Debug.Log($"회원가입 요청 전송 - ID: {id}, ProfileIndex: {currentSelectedIndex}");
    }
}


# --- File: Assets\Script\Server\ClientSimpleTcp.cs ---
﻿using System;
using System.Net.Sockets;
using System.Net;
using UnityEditor.XR;

namespace ChatClient2
{
    public class ClientSimpleTcp
    {        

        public Socket Sock = null;   
        public string LatestErrorMsg;      
               
        //소켓연결        
        public bool Connect(string ip, int port)
        {
            try
            {
                IPAddress serverIP = IPAddress.Parse(ip);
                int serverPort = port;

                Sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                Sock.Connect(new IPEndPoint(serverIP, serverPort));

                if (Sock == null || Sock.Connected == false)
                {
                    return false;
                }
                
                return true;
            }
            catch (Exception ex)
            {
                LatestErrorMsg = ex.Message;
                return false;
            }
        }

        public Tuple<int,byte[]> Receive()
        {

            try
            {
                byte[] ReadBuffer = new byte[2048];
                var nRecv = Sock.Receive(ReadBuffer, 0, ReadBuffer.Length, SocketFlags.None);

                if (nRecv == 0)
                {
                    return null;
                }

                return Tuple.Create(nRecv,ReadBuffer);
            }
            catch (SocketException se)
            {
                LatestErrorMsg = se.Message;
            }

            return null;
        }

        //스트림에 쓰기
        public void Send(byte[] sendData)
        {
            try
            {
                if (Sock != null && Sock.Connected) //연결상태 유무 확인
                {
                    Sock.Send(sendData, 0, sendData.Length, SocketFlags.None);
                }
                else
                {
                    LatestErrorMsg = "먼저 채팅서버에 접속하세요!";
                }
            }
            catch (SocketException se)
            {
                LatestErrorMsg = se.Message;
            }
        }

        //소켓과 스트림 닫기
        public void Close()
        {
            if (Sock != null && Sock.Connected)
            {
                //Sock.Shutdown(SocketShutdown.Both);
                Sock.Close();
            }
        }

        public bool IsConnected() { return (Sock != null && Sock.Connected) ? true : false; }
    }
}


# --- File: Assets\Script\Server\LoginUI.cs ---
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

    void Start()
    {
        // 버튼에 함수 연결
        loginButton.onClick.AddListener(OnClickLogin);
        registerButton.onClick.AddListener(OnClickRegister);

        // NetworkManager 이벤트 구독 (서버 응답 오면 실행될 함수들)
        NetworkManager.Instance.OnLoginResult += HandleLoginResult;
        NetworkManager.Instance.OnCreateAccountResult += HandleRegisterResult;
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


# --- File: Assets\Script\Server\NetworkManager.cs ---
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using ChatClient2;
using CSBaseLib;
using MessagePack;
using UnityEditor.PackageManager;
using UnityEngine;

// 서버와 통신을 담당하는 핵심 매니저 클래스
public sealed class NetworkManager
{
    // 싱글톤 패턴 구현
    private static readonly Lazy<NetworkManager> _instance = new(() => new NetworkManager());
    public static NetworkManager Instance => _instance.Value;

    private bool _isInitialized = false;

    // TCP 통신 래퍼 클래스
    ClientSimpleTcp Network = new ClientSimpleTcp();

    // 스레드 제어 플래그
    bool IsNetworkThreadRunning = false;
    bool IsBackGroundProcessRunning = false;

    // =================================================================
    // [UI 연동을 위한 이벤트 (Action)]
    // UI 스크립트에서 이 이벤트들을 구독(Subscribe)하여 화면을 갱신합니다.
    // =================================================================
    public Action<bool> OnLoginResult;                 // 로그인 성공/실패 알림
    public Action<string, string, int> OnChatReceived;
    public Action<List<RankingData>> OnRankingReceived; // 랭킹 리스트 수신
    public Action<int> OnScoreReceived;                // 점수 획득 결과 알림 (현재 점수)
    public Action<bool> OnCreateAccountResult;


    // 스레드 정의
    System.Threading.Thread NetworkReadThread = null;
    System.Threading.Thread NetworkSendThread = null;
    System.Threading.Thread BackGroundProcessThread = null;

    // 패킷 버퍼 및 큐
    PacketBufferManager PacketBuffer = new PacketBufferManager();
    Queue<PacketData> RecvPacketQueue = new Queue<PacketData>();
    Queue<byte[]> SendPacketQueue = new Queue<byte[]>();


    private NetworkManager() { }

    // 초기화 및 서버 연결
    public void Initialize()
    {
        if (_isInitialized) return;

        // 패킷 버퍼 초기화
        PacketBuffer.Init((8096 * 10), PacketDef.HeaderSize, 1024);

        // 스레드 시작
        IsNetworkThreadRunning = true;
        NetworkReadThread = new System.Threading.Thread(this.NetworkReadProcess);
        NetworkReadThread.Start();
        NetworkSendThread = new System.Threading.Thread(this.NetworkSendProcess);
        NetworkSendThread.Start();

        IsBackGroundProcessRunning = true;
        BackGroundProcessThread = new System.Threading.Thread(this.BackGroundProcess);
        BackGroundProcessThread.Start();

        // 서버 연결 시도 (IP와 Port는 서버 설정에 맞게 변경)
        bool bNetwork = Network.Connect("127.0.0.1", 32452);

        if (bNetwork)
        {
            Debug.Log("서버에 접속 성공 !!!");
        }
        else
        {
            Debug.LogError("서버에 접속 실패 !!!");
        }

        _isInitialized = true;
    }

    // 서버 연결 종료
    public void Stop()
    {
        IsNetworkThreadRunning = false;
        IsBackGroundProcessRunning = false;
        Network.Close();
    }

    // =================================================================
    // [패킷 전송 함수 (Client -> Server)]
    // UI나 게임 로직에서 호출하는 함수들입니다.
    // =================================================================

    // 1. 로그인 요청
    public void SendLogin(string userId, string authToken)
    {
        var request = new PKReqLogin { UserID = userId, AuthToken = authToken };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_LOGIN, body);
        PostSendPacket(sendData);
    }

    // 2. 채팅 메시지 전송
    public void SendChat(string message)
    {
        var request = new PKTReqRoomChat { ChatMessage = message };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_ROOM_CHAT, body);
        PostSendPacket(sendData);
    }

    // 3. 랭킹 리스트 요청
    public void RequestRanking()
    {
        // 요청 패킷 생성 (UserID는 현재 로그인한 유저 정보 활용)
        var request = new PKTReqUserRankingList { UserID = PlayerManager.instance.UserID };
        var body = MessagePackSerializer.Serialize(request);

        // REQ_USER_RANKING_LIST (1105) 패킷 ID 사용
        var sendData = PacketToBytes.Make(PacketId.REQ_USER_RANKING_LIST, body);
        PostSendPacket(sendData);

        Debug.Log("서버에 랭킹 리스트를 요청했습니다.");
    }

    // 4. 점수 획득 (무기 제작 성공 시 호출)
    public void SendScoreAdd(string userId, int scoreIncrease)
    {
        var request = new PKTReqUserScoreAdd { UserID = userId, AddScore = scoreIncrease };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_USER_SCORE_ADD, body);
        PostSendPacket(sendData);
    }

    // 패킷 큐에 데이터 등록
    public void PostSendPacket(byte[] sendData)
    {
        if (Network.IsConnected() == false)
        {
            Debug.LogWarning("서버 연결이 되어 있지 않습니다");
            return;
        }
        lock (((System.Collections.ICollection)SendPacketQueue).SyncRoot)
        {
            SendPacketQueue.Enqueue(sendData);
        }
    }

    // =================================================================
    // [패킷 수신 처리 (Server -> Client)]
    // 백그라운드 스레드에서 패킷을 꺼내 처리합니다.
    // =================================================================
    void BackGroundProcess()
    {
        while (IsBackGroundProcessRunning)
        {
            try
            {
                var packet = new PacketData();
                lock (((System.Collections.ICollection)RecvPacketQueue).SyncRoot)
                {
                    if (RecvPacketQueue.Count() > 0)
                    {
                        packet = RecvPacketQueue.Dequeue();
                    }
                    else
                    {
                        // 큐가 비었으면 잠시 대기
                        Thread.Sleep(1);
                        continue;
                    }
                }

                if (packet.PacketID != 0)
                {
                    PacketProcess(packet);
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"Packet Process Error: {ex.Message}");
            }
        }
    }

    // 실제 패킷 로직 처리 (Switch문)
    void PacketProcess(PacketData packet)
    {
        switch ((PacketId)packet.PacketID)
        {
            // 1. 로그인 응답 처리
            case PacketId.RES_LOGIN:
                {
                    var resData = MessagePackSerializer.Deserialize<PKResLogin>(packet.BodyData);
                    Debug.Log($"[Login] Result: {resData.Result}, ID: {resData.UserID}");

                    // 메인 스레드(UI)로 이벤트 전달
                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            bool isSuccess = (resData.Result == (short)CSBaseLib.ErrorCode.NONE);
                            OnLoginResult?.Invoke(isSuccess);
                        });
                    }
                }
                break;

            // 2. 채팅 수신 (브로드캐스트)
            case PacketId.NTF_ROOM_CHAT:
                {
                    var ntfData = MessagePackSerializer.Deserialize<PKTNtfRoomChat>(packet.BodyData);

                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            // ntfData에서 ProfileIndex도 함께 꺼내서 Invoke 합니다.
                            OnChatReceived?.Invoke(ntfData.UserID, ntfData.ChatMessage, ntfData.ProfileIndex);
                        });
                    }
                }
                break;

            // 3. 랭킹 리스트 수신
            case PacketId.RES_USER_RANKING_LIST:
                {
                    var resData = MessagePackSerializer.Deserialize<PKTResUserRankingList>(packet.BodyData);

                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            OnRankingReceived?.Invoke(resData.RankList);
                        });
                    }
                }
                break;

            // 4. 점수 획득 결과 수신
            case PacketId.RES_USER_SCORE_ADD:
                {
                    var resData = MessagePackSerializer.Deserialize<PKTResUserScoreAdd>(packet.BodyData);
                    Debug.Log($"[Score] Final Score: {resData.FinalScore}");

                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            OnScoreReceived?.Invoke(resData.FinalScore);
                        });
                    }
                }
                break;
            case PacketId.RES_CREATE_ACCOUNT:
                {
                    var resData = MessagePackSerializer.Deserialize<PKResCreateAccount>(packet.BodyData);

                    if (UnityMainThreadDispatcher.Instance != null)
                    {
                        UnityMainThreadDispatcher.Instance.Enqueue(() =>
                        {
                            bool isSuccess = (resData.Result == (short)CSBaseLib.ErrorCode.NONE);
                            if (isSuccess) Debug.Log("회원가입 성공!");
                            else Debug.Log("회원가입 실패: 중복된 ID입니다.");

                            // UI에 결과 알림
                            OnCreateAccountResult?.Invoke(isSuccess);
                        });
                    }
                }
                break;
        }
    }

    public void SendCreateAccount(string userId, string password, int profileIndex)
    {
        var request = new PKReqCreateAccount
        {
            UserID = userId,
            Password = password,
            ProfileIndex = profileIndex // 패킷 데이터에 포함
        };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_CREATE_ACCOUNT, body);
        PostSendPacket(sendData);
    }


    // =================================================================
    // [네트워크 로우 레벨 처리 (Read/Write)]
    // =================================================================
    void NetworkReadProcess()
    {
        while (IsNetworkThreadRunning)
        {
            if (Network.IsConnected() == false)
            {
                Thread.Sleep(10);
                continue;
            }

            var recvData = Network.Receive();

            if (recvData != null)
            {
                // 버퍼에 데이터 쓰기
                PacketBuffer.Write(recvData.Item2, 0, recvData.Item1);

                while (true)
                {
                    // 버퍼에서 패킷 완성본 읽기
                    var data = PacketBuffer.Read();
                    if (data.Count < 1) break;

                    var packet = new PacketData();
                    packet.DataSize = (short)(data.Count - PacketDef.HeaderSize);
                    packet.PacketID = BitConverter.ToInt16(data.Array, data.Offset + 2);
                    packet.Type = (SByte)data.Array[(data.Offset + 4)];
                    packet.BodyData = new byte[packet.DataSize];
                    Buffer.BlockCopy(data.Array, (data.Offset + PacketDef.HeaderSize), packet.BodyData, 0, packet.DataSize);

                    lock (((System.Collections.ICollection)RecvPacketQueue).SyncRoot)
                    {
                        RecvPacketQueue.Enqueue(packet);
                    }
                }
            }
            else
            {
                // 수신 데이터가 null이면 연결 끊김으로 간주
                // 필요 시 재연결 로직 추가 가능
            }
        }
    }

    void NetworkSendProcess()
    {
        while (IsNetworkThreadRunning)
        {
            if (Network.IsConnected() == false)
            {
                Thread.Sleep(10);
                continue;
            }

            lock (((System.Collections.ICollection)SendPacketQueue).SyncRoot)
            {
                if (SendPacketQueue.Count > 0)
                {
                    var packet = SendPacketQueue.Dequeue();
                    Network.Send(packet);
                }
            }
            Thread.Sleep(1);
        }
    }

    public void RequestUserScore(string userId)
    {
        var request = new PKTReqUserScoreGet { UserID = userId };
        var body = MessagePackSerializer.Serialize(request);
        var sendData = PacketToBytes.Make(PacketId.REQ_USER_SCORE_GET, body);
        PostSendPacket(sendData);
    }
}

# --- File: Assets\Script\Server\PacketBufferManager.cs ---
﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChatClient2
{
    class PacketBufferManager
    {
        int BufferSize = 0;
        int ReadPos = 0;
        int WritePos = 0;

        int HeaderSize = 0;
        int MaxPacketSize = 0;
        byte[] PacketData;
        byte[] PacketDataTemp;

        public bool Init(int size, int headerSize, int maxPacketSize)
        {
            if (size < (maxPacketSize * 2) || size < 1 || headerSize < 1 || maxPacketSize < 1)
            {
                return false;
            }

            BufferSize = size;
            PacketData = new byte[size];
            PacketDataTemp = new byte[size];
            HeaderSize = headerSize;
            MaxPacketSize = maxPacketSize;

            return true;
        }

        public bool Write(byte[] data, int pos, int size)
        {
            if (data == null || (data.Length < (pos + size)))
            {
                return false;
            }

            var remainBufferSize = BufferSize - WritePos;

            if (remainBufferSize < size)
            {
                return false;
            }

            Buffer.BlockCopy(data, pos, PacketData, WritePos, size);
            WritePos += size;

            if (NextFree() == false)
            {
                BufferRelocate();
            }
            return true;
        }

        public ArraySegment<byte> Read()
        {
            var enableReadSize = WritePos - ReadPos;

            if (enableReadSize < HeaderSize)
            {
                return new ArraySegment<byte>();
            }

            var packetDataSize = BitConverter.ToInt16(PacketData, ReadPos);
            if (enableReadSize < packetDataSize)
            {
                return new ArraySegment<byte>();
            }

            var completePacketData = new ArraySegment<byte>(PacketData, ReadPos, packetDataSize);
            ReadPos += packetDataSize;
            return completePacketData;
        }

        bool NextFree()
        {
            var enableWriteSize = BufferSize - WritePos;

            if (enableWriteSize < MaxPacketSize)
            {
                return false;
            }

            return true;
        }

        void BufferRelocate()
        {
            var enableReadSize = WritePos - ReadPos;

            Buffer.BlockCopy(PacketData, ReadPos, PacketDataTemp, 0, enableReadSize);
            Buffer.BlockCopy(PacketDataTemp, 0, PacketData, 0, enableReadSize);

            ReadPos = 0;
            WritePos = enableReadSize;
        }
    }
}


# --- File: Assets\Script\Server\PacketData.cs ---
﻿using MessagePack; //https://github.com/neuecc/MessagePack-CSharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSBaseLib
{
    public struct PacketData
    {
        public Int16 DataSize;
        public Int16 PacketID;
        public SByte Type;
        public byte[] BodyData;
    }
    public class PacketDef
    {
        public const Int16 HeaderSize = 5;
        public const int MAX_USER_ID_BYTE_LENGTH = 16;
        public const int MAX_USER_PW_BYTE_LENGTH = 16;

        public const int INVALID_ROOM_NUMBER = -1;
    }

    public class PacketToBytes
    {
        public static byte[] Make(PacketId packetID, byte[] bodyData)
        {
            byte type = 0;
            var pktID = (UInt16)packetID;
            UInt16 bodyDataSize = 0;
            if (bodyData != null)
            {
                bodyDataSize = (UInt16)bodyData.Length;
            }
            var packetSize = (UInt16)(bodyDataSize + PacketDef.HeaderSize);
                        
            var dataSource = new byte[packetSize];
            Buffer.BlockCopy(BitConverter.GetBytes(packetSize), 0, dataSource, 0, 2);
            Buffer.BlockCopy(BitConverter.GetBytes(pktID), 0, dataSource, 2, 2);
            dataSource[4] = type;
            
            if (bodyData != null)
            {
                Buffer.BlockCopy(bodyData, 0, dataSource, 5, bodyDataSize);
            }

            return dataSource;
        }

        public static Tuple<int, byte[]> ClientReceiveData(int recvLength, byte[] recvData)
        {
            var packetSize = BitConverter.ToUInt16(recvData, 0);
            var packetID = BitConverter.ToUInt16(recvData, 2);
            var bodySize = packetSize - PacketDef.HeaderSize;

            var packetBody = new byte[bodySize];
            Buffer.BlockCopy(recvData, PacketDef.HeaderSize, packetBody,  0, bodySize);

            return new Tuple<int, byte[]>(packetID, packetBody);
        }
    }

    [MessagePackObject]
    public class PKReqLogin
    {
        [Key(0)] public string UserID;
        [Key(1)] public string AuthToken;
    }

    [MessagePackObject]
    public class PKResLogin
    {
        [Key(0)] public short Result; // ErrorCode
        [Key(1)] public string UserID;
        [Key(2)] public int CurrentScore;
    }

    // --- [점수 추가] ---
    [MessagePackObject]
    public class PKTReqUserScoreAdd
    {
        [Key(0)] public string UserID;
        [Key(1)] public int AddScore;
    }

    [MessagePackObject]
    public class PKTResUserScoreAdd
    {
        [Key(0)] public short Result;
        [Key(1)] public int FinalScore;
    }

    // --- [랭킹] ---
    [MessagePackObject]
    public class PKTReqUserRankingList
    {
        [Key(0)] public string UserID;
    }

    [MessagePackObject]
    public class PKTResUserRankingList
    {
        [Key(0)] public List<RankingData> RankList;
    }

    [MessagePackObject]
    public class RankingData
    {
        [Key(0)] public string UserID;
        [Key(1)] public int Score;
        [Key(2)] public int Rank;
        [Key(3)] public int ProfileIndex;
    }

    // --- [채팅] ---
    [MessagePackObject]
    public class PKTReqRoomChat
    {
        [Key(0)] public string ChatMessage;
    }

    [MessagePackObject]
    public class PKTNtfRoomChat
    {
        [Key(0)] public string UserID;
        [Key(1)] public string ChatMessage;
        [Key(2)]
        public int ProfileIndex;
    }
    [MessagePackObject] public class PKTReqUserScoreGet { [Key(0)] public string UserID; }
    [MessagePackObject] public class PKTResUserScoreGet { [Key(0)] public short Result; [Key(1)] public int Score; }

    [MessagePackObject]
    public class PKReqCreateAccount
    {
        [Key(0)] public string UserID;
        [Key(1)] public string Password; // AuthToken 대신 Password 사용
        [Key(2)]
        public int ProfileIndex;
    }

    // [추가] 회원가입 응답
    [MessagePackObject]
    public class PKResCreateAccount
    {
        [Key(0)] public short Result; // ErrorCode
    }
}


# --- File: Assets\Script\Server\PacketDefine.cs ---
﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSBaseLib
{
    // 0 ~ 9999
    public enum ErrorCode : short
    {
        NONE = 0,

        // 서버 초기화 에라
        REDIS_INIT_FAIL = 1,    // Redis 초기화 에러

        // 로그인 
        LOGIN_FAILED = 1001,
        DB_ERROR = 1002,
        REMOVE_USER_SEARCH_FAILURE_USER_ID = 1003,
        USER_AUTH_SEARCH_FAILURE_USER_ID = 1004,
        USER_AUTH_ALREADY_SET_AUTH = 1005,
        LOGIN_ALREADY_WORKING = 1006,
        LOGIN_FULL_USER_COUNT = 1007,

        DB_LOGIN_INVALID_PASSWORD = 1011,
        DB_LOGIN_EMPTY_USER = 1012,
        DB_LOGIN_EXCEPTION = 1013,

        ROOM_ENTER_INVALID_STATE = 1021,
        ROOM_ENTER_INVALID_USER = 1022,
        ROOM_ENTER_ERROR_SYSTEM = 1023,
        ROOM_ENTER_INVALID_ROOM_NUMBER = 1024,
        ROOM_ENTER_FAIL_ADD_USER = 1025,

        CREATE_FAIL_DUPLICATE = 2001, // 이미 존재하는 아이디
    }

    // 1 ~ 10000
    public enum PacketId : int
    {
        REQ_RES_TEST_ECHO = 101,


        // 클라이언트
        CS_BEGIN = 1001,

        REQ_LOGIN = 1002,
        RES_LOGIN = 1003,
        NTF_MUST_CLOSE = 1005,

        REQ_CREATE_ACCOUNT = 1008,
        RES_CREATE_ACCOUNT = 1009,

        REQ_ROOM_ENTER = 1015,
        RES_ROOM_ENTER = 1016,
        NTF_ROOM_USER_LIST = 1017,
        NTF_ROOM_NEW_USER = 1018,

        REQ_ROOM_LEAVE = 1021,
        RES_ROOM_LEAVE = 1022,
        NTF_ROOM_LEAVE_USER = 1023,

        REQ_ROOM_CHAT = 1026,
        NTF_ROOM_CHAT = 1027,


        REQ_ROOM_DEV_ALL_ROOM_START_GAME = 1091,
        RES_ROOM_DEV_ALL_ROOM_START_GAME = 1092,

        REQ_ROOM_DEV_ALL_ROOM_END_GAME = 1093,
        RES_ROOM_DEV_ALL_ROOM_END_GAME = 1094,

        REQ_USER_ACCESSION = 1095,
        RES_USER_ACCESSION = 1096,

        REQ_USER_INFO_UPDATE = 1097,
        RES_USER_INFO_UPDATE = 1098,

        REQ_USER_INFO_DELETE = 1099,
        RES_USER_INFO_DELETE = 1100,

        REQ_USER_SEARCH = 1101,
        RES_USER_SEARCH = 1102,

        REQ_USER_SCORE_UPDATE = 1103,
        RES_USER_SCORE_UPDATE = 1104,

        REQ_USER_RANKING_LIST = 1105,
        RES_USER_RANKING_LIST = 1106,
        REQ_USER_SCORE_GET = 1107, // [추가됨] 점수 조회 요청
        RES_USER_SCORE_GET = 1108,
        REQ_USER_SCORE_ADD = 1109,    // 점수 획득 (Redis Ranking)
        RES_USER_SCORE_ADD = 1110,

        CS_END = 1200,


        // 시스템, 서버 - 서버
        SS_START = 8001,

        NTF_IN_CONNECT_CLIENT = 8011,
        NTF_IN_DISCONNECT_CLIENT = 8012,

        REQ_SS_SERVERINFO = 8021,
        RES_SS_SERVERINFO = 8023,

        REQ_IN_ROOM_ENTER = 8031,
        RES_IN_ROOM_ENTER = 8032,

        NTF_IN_ROOM_LEAVE = 8036,


        // DB 8101 ~ 9000
        REQ_DB_LOGIN = 8101,
        RES_DB_LOGIN = 8102,
    }

    
    
}


# --- File: Assets\Script\Server\Prifile.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ProfileSelector : MonoBehaviour
{
    public int SelectedIndex = 0; // 현재 선택된 인덱스 (기본값 0)
    public Image[] profileButtons; // UI의 버튼 이미지 배열

    public void SelectProfile(int index)
    {
        SelectedIndex = index;
        // 선택 시 시각적 효과 (예: 테두리 강조 등)를 여기에 추가할 수 있습니다.
        Debug.Log($"선택된 프로필 인덱스: {SelectedIndex}");
    }
}


# --- File: Assets\Script\Server\RankingItem.cs ---
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class RankingItem : MonoBehaviour
{
    public TextMeshProUGUI rankText;
    public Image profileImage;
    public TextMeshProUGUI idText;
    public TextMeshProUGUI scoreText;
    public Sprite[] profileSprites;

    public void SetInfo(int rank, string id, int score, int profileIdx)
    {
        rankText.text = rank.ToString();
        idText.text = id;
        scoreText.text = score.ToString();
        if (profileIdx >= 0 && profileIdx < profileSprites.Length)
            profileImage.sprite = profileSprites[profileIdx];
    }
}


# --- File: Assets\Script\Server\RankingManager.cs ---
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
        // 유니티 UI 업데이트는 반드시 메인 스레드에서 실행되어야 함
        UnityMainThreadDispatcher.Instance.Enqueue(() =>
        {
            // 기존에 생성되어 있던 랭킹 아이템들 삭제
            foreach (Transform child in rankingContent)
            {
                Destroy(child.gameObject);
            }

            // 서버에서 받은 데이터를 순서대로 프리팹으로 생성
            foreach (var data in rankList)
            {
                GameObject newItem = Instantiate(rankingItemPrefab, rankingContent);
                RankingItem itemScript = newItem.GetComponent<RankingItem>();

                if (itemScript != null)
                {
                    // 순위, 아이디, 점수, 프로필 인덱스 설정
                    itemScript.SetInfo(data.Rank, data.UserID, data.Score, data.ProfileIndex);
                }
            }

            Debug.Log("랭킹 UI 갱신 완료");
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


# --- File: Assets\Script\Server\ServerLauncher.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkConnector : MonoBehaviour
{
    [Header("Network Settings")]
    public string serverIP = "127.0.0.1";
    public int serverPort = 32452;

    void Awake()
    {
        // 1. 이미 초기화되었는지 확인 (혹시라도 씬을 다시 로드했을 때 방지)
        // NetworkManager 내부에 _isInitialized 체크가 있지만 여기서 한 번 더 해도 좋음

        // 2. 서버 매니저 초기화 및 접속 시도
        // (참고: NetworkManager.Initialize() 내부에서 Connect할 때 인자를 받도록 수정하거나,
        //  Network.Connect(serverIP, serverPort)를 호출하는 방식을 맞춰야 함)

        // 현재 NetworkManager 코드에는 IP/Port를 내부에서 "127.0.0.1"로 고정하고 있습니다.
        // 유연성을 위해 Initialize 호출 전이나 후에 IP를 설정하거나,
        // Initialize 함수가 IP, Port를 받도록 수정하는 것이 좋습니다.

        NetworkManager.Instance.Initialize();

        Debug.Log("네트워크 매니저 초기화 요청됨");
    }

    // ★★★ 가장 중요 ★★★
    // 이게 없으면 유니티 에디터에서 플레이 멈춤 눌러도
    // 백그라운드 스레드(NetworkReadThread)가 계속 살아서 에러를 뿜거나 유니티가 멈춥니다.
    void OnApplicationQuit()
    {
        NetworkManager.Instance.Stop();
        Debug.Log("네트워크 매니저 종료 및 스레드 정리됨");
    }
}


# --- File: Assets\Script\Server\UnityMainThreadDispatcher.cs ---
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class UnityMainThreadDispatcher : MonoBehaviour
{
    private static readonly Queue<Action> _executionQueue = new Queue<Action>();
    public static UnityMainThreadDispatcher Instance { get; private set; }

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    // Unity의 메인 스레드에서 매 프레임 실행됨
    void Update()
    {
        lock (_executionQueue)
        {
            while (_executionQueue.Count > 0)
            {
                // 큐에서 작업을 꺼내 메인 스레드에서 실행
                _executionQueue.Dequeue().Invoke();
            }
        }
    }

    // 백그라운드 스레드에서 호출하여 작업을 큐에 추가하는 함수
    public void Enqueue(Action action)
    {
        if (action == null) return;
        lock (_executionQueue)
        {
            _executionQueue.Enqueue(action);
        }
    }
}


# --- File: Assets\Script\UI\ChatItem.cs ---
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class ChatItem : MonoBehaviour
{
    public Image profileImage;      // 프로필 아이콘 이미지
    public TextMeshProUGUI nameText; // 유저 이름 텍스트
    public TextMeshProUGUI msgText;  // 채팅 내용 텍스트

    public Sprite[] profileSprites; // 미리 등록해둔 프로필 스프라이트 배열 (0~4)

    public void SetChat(string name, string message, int profileIndex)
    {
        nameText.text = name;
        msgText.text = message;

        // 인덱스 범위 체크 후 이미지 교체
        if (profileIndex >= 0 && profileIndex < profileSprites.Length)
        {
            profileImage.sprite = profileSprites[profileIndex];
        }
    }
}


# --- File: Assets\Script\UI\ChatManager.cs ---
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using System;

public class ChatManager : MonoBehaviour
{
    public TMP_InputField chatInputField; // 입력창
    public Transform chatContent;         // ScrollView의 Content (프리팹이 생성될 부모)
    public GameObject chatItemPrefab;     // 채팅 바 프리팹

    void Start()
    {
        // 서버로부터 채팅 알림을 받았을 때 실행될 이벤트 구독
        NetworkManager.Instance.OnChatReceived += AddChatLog;
    }

    // 전송 버튼 클릭 시 호출
    public void OnClickSend()
    {
        if (string.IsNullOrEmpty(chatInputField.text)) return;

        // 서버로 채팅 요청 전송
        NetworkManager.Instance.SendChat(chatInputField.text);
        chatInputField.text = ""; // 입력창 초기화
    }

    // 서버 알림 패킷 수신 시 호출 (UnityMainThreadDispatcher 활용 필수)
    public void AddChatLog(string userId, string message, int profileIndex)
    {
        // 메인 스레드에서 UI 생성
        UnityMainThreadDispatcher.Instance.Enqueue(() =>
        {
            GameObject newChat = Instantiate(chatItemPrefab, chatContent);
            ChatItem item = newChat.GetComponent<ChatItem>();

            // 데이터 설정
            item.SetChat(userId, message, profileIndex);

            // 스크롤을 최하단으로 내리는 로직을 여기에 추가할 수 있습니다.
        });
    }
}


# --- File: Assets\Script\UI\ScoreDisplay.cs ---
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


