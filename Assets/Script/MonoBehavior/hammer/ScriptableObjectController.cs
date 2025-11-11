using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScriptableObjectController : MonoBehaviour
{
    public PlayerManager playerManager;

    // ±³Ã¼ÇÒ ScriptableObject
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
