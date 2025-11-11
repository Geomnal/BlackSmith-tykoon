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
