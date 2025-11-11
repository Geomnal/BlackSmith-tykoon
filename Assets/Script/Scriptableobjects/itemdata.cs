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
