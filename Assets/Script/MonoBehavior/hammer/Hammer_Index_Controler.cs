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
