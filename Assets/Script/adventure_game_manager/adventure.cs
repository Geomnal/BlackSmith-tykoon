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
