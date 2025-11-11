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