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

