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
