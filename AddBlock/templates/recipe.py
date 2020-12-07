TEMPLATE_RECIPE = '''
{
    "type": "minecraft:crafting_shaped",
    "pattern": [
        "ccc",
        "c#c",
        "ccc"
    ],
    "key": {
        "c": {
            "item": "minecraft:clay"
        },
        "#": {
            "tag": "forge:ingots/iron"
        }
    },
    "result": {
        "item": "$[modid]:$L[name]"
    }
}
'''