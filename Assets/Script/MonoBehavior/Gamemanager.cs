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

