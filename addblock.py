from typing import Dict, Any
from argparse import ArgumentParser
from pathlib import Path
import json

#################################################################################
# CONFIG
#################################################################################
MODID_REF = 'RFToolsStorage.MODID'
MODID = 'rftoolsstorage'

ROOT_PACKAGE = 'mcjty.rftoolsstorage'
SOURCE_ROOT = Path('src/main/java/mcjty/rftoolsstorage')
ASSET_RESOURCE_ROOT = Path('src/main/resources/assets/rftoolsstorage')
DATA_RESOURCE_ROOT = Path('src/main/resources/data/rftoolsstorage')

PACKAGE_BLOCKS = 'blocks'
PACKAGE_TILES = 'tiles'
PACKAGE_CONTAINERS = 'containers'
PACKAGE_SCREENS = 'screens'
#################################################################################
#################################################################################
# Templates
#################################################################################
TEMPLATE_BLOCK_JAVA = '''
package $[package];

import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.material.Material;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.inventory.container.Container;
import net.minecraft.inventory.container.INamedContainerProvider;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.Hand;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.BlockRayTraceResult;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TranslationTextComponent;
import net.minecraft.world.IBlockReader;
import net.minecraft.world.World;
import net.minecraftforge.fml.network.NetworkHooks;

import javax.annotation.Nullable;

public class $[name]Block extends Block {

    public $[name]Block() {
        super(Properties.create(Material.IRON));
    }
    ?{tile

    @Override
    public boolean hasTileEntity(BlockState state) {
        return true;
    }

    @Nullable
    @Override
    public TileEntity createTileEntity(BlockState state, IBlockReader world) {
        return new $[name]Tile();
    }
    ?}tile
    ?{gui

    @Override
    public boolean onBlockActivated(BlockState state, World world, BlockPos pos, PlayerEntity player, Hand hand, BlockRayTraceResult result) {
        if (!world.isRemote) {
            NetworkHooks.openGui((ServerPlayerEntity) player, new INamedContainerProvider() {
                @Override
                public ITextComponent getDisplayName() {
                    return new TranslationTextComponent("title.from.langfile"); // Put your own title description here
                }

                @Nullable
                @Override
                public Container createMenu(int i, PlayerInventory playerInventory, PlayerEntity playerEntity) {
                    return new $[name]Container(i, world, pos, playerInventory, playerEntity);
                }
            }, pos);
            return true;
        }
        return super.onBlockActivated(state, world, pos, player, hand, result);
    }
    ?}gui
}
/*
====== Code to move to your objectholder class ======

@ObjectHolder($[modid_ref]+":$L[name]")
public static $[name]Block $U[name];

====== Code to move to your registration event class ======

@SubscribeEvent
public static void onBlockRegister(final RegistryEvent.Register<Block> e) {
    e.getRegistry().register(new $[name]Block().setRegistryName("$L[name]");
}
*/
'''
TEMPLATE_TILE_JAVA = '''
package $[package];

import net.minecraft.nbt.CompoundNBT;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.Direction;
import net.minecraftforge.common.capabilities.Capability;
import net.minecraftforge.common.util.INBTSerializable;
import net.minecraftforge.common.util.LazyOptional;
import net.minecraftforge.items.CapabilityItemHandler;
import net.minecraftforge.items.IItemHandler;
import net.minecraftforge.items.ItemStackHandler;

import javax.annotation.Nonnull;
import javax.annotation.Nullable;

public class $[name]Tile extends TileEntity {
    ?{gui
    private LazyOptional<IItemHandler> handler = LazyOptional.of(this::createHandler);
    ?}gui

    public $[name]Tile() {
        super($U[name]_TILE);
    }
    ?{gui

    @Override
    public void read(CompoundNBT tag) {
        CompoundNBT invTag = tag.getCompound("inv");
        handler.ifPresent(h -> ((INBTSerializable<CompoundNBT>) h).deserializeNBT(invTag));
    }

    @Override
    public CompoundNBT write(CompoundNBT tag) {
        handler.ifPresent(h -> {
            CompoundNBT compound = ((INBTSerializable<CompoundNBT>) h).serializeNBT();
            tag.put("inv", compound);
        });
        return super.write(tag);
    }

    private IItemHandler createHandler() {
        return new ItemStackHandler($[name]Container.COUNT) {

            @Override
            protected void onContentsChanged(int slot) {
                markDirty();
            }
        };
    }

    @Nonnull
    @Override
    public <T> LazyOptional<T> getCapability(@Nonnull Capability<T> cap, @Nullable Direction side) {
        if (cap == CapabilityItemHandler.ITEM_HANDLER_CAPABILITY) {
            return handler.cast();
        }
        return super.getCapability(cap, side);
    }
    ?}gui
}
/*
====== Code to move to your objectholder class ======

@ObjectHolder($[modid_ref]+":$L[name]")
public static TileEntityType<$[name]Tile> $U[name]_TILE;

====== Code to move to your registration event class ======

@SubscribeEvent
public static void onTileRegister(final RegistryEvent.Register<TileEntityType<?>> e) {
    e.getRegistry().register(TileEntityType.Builder.create($[name]Tile::new, $U[name]BLOCK).build(null).setRegistryName("$L{name}"));
}
*/
'''
TEMPLATE_CONTAINER_JAVA = '''
package $[package];

import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.container.Container;
import net.minecraft.inventory.container.Slot;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.IWorldPosCallable;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.items.CapabilityItemHandler;
import net.minecraftforge.items.SlotItemHandler;

public class $[name]Container extends Container {
    public static final int COUNT = 1;      // Change for a different number of slots in this container

    private TileEntity tileEntity;
    private PlayerEntity playerEntity;

    public $[name]Container(int windowId, World world, BlockPos pos, PlayerInventory playerInventory, PlayerEntity player) {
        super($U[name]_CONTAINER, windowId);
        tileEntity = world.getTileEntity(pos);
        this.playerEntity = player;

        tileEntity.getCapability(CapabilityItemHandler.ITEM_HANDLER_CAPABILITY).ifPresent(h -> {
            // Add more slots here if needed
            addSlot(new SlotItemHandler(h, 0, 64, 24));
        });
        layoutPlayerInventorySlots(playerInventory, 10, 70);
    }

    @Override
    public boolean canInteractWith(PlayerEntity playerIn) {
        return isWithinUsableDistance(IWorldPosCallable.of(tileEntity.getWorld(), tileEntity.getPos()), playerEntity, $U{name});
    }

    private void layoutPlayerInventorySlots(PlayerInventory playerInventory, int leftCol, int topRow) {
        // Player inventory
        int index = 9;
        int y = topRow;
        for (int j = 0; j < 3; j++) {
            int x = leftCol;
            for (int i = 0; i < 9; i++) {
                addSlot(new Slot(playerInventory, index++, x, y));
                x += 18;
            }
            y += 18;
        }

        // Hotbar
        topRow += 58;
        index = 0;
        int x = leftCol;
        for (int i = 0; i < 9; i++) {
            addSlot(new Slot(playerInventory, index++, x, topRow));
            x += 18;
        }
    }

    @Override
    public ItemStack transferStackInSlot(PlayerEntity playerIn, int index) {
        // TODO provide a proper implementation here depending on what you need!
        return ItemStack.EMPTY;
    }
}
/*
====== Code to move to your objectholder class ======

@ObjectHolder($[modid_ref]+":$L[name]")
public static ContainerType<$[name]Container> $U[name]_CONTAINER;

====== Code to move to your registration event class ======

@SubscribeEvent
public static void onContainerRegister(final RegistryEvent.Register<ContainerType<?>> e) {
    e.getRegistry().register(IForgeContainerType.create((windowId, inv, data) -> {
        BlockPos pos = data.readBlockPos();
        World clientWorld = DistExecutor.runForDist(() -> () -> Minecraft.getInstance().world, () -> () -> null);
        PlayerEntity clientPlayer = DistExecutor.runForDist(() -> () -> Minecraft.getInstance().player, () -> () -> null);
        return new $[name]Container(windowId, clientWorld, pos, inv, clientPlayer);
    }).setRegistryName("$L[name]"));
}
*/
'''
TEMPLATE_SCREEN_JAVA = '''
package $[package];

import com.mojang.blaze3d.platform.GlStateManager;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screen.inventory.ContainerScreen;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.text.ITextComponent;

public class $[name]Screen extends ContainerScreen<$[name]Container> {
    private ResourceLocation GUI = new ResourceLocation($[modid_ref], "textures/gui/$L[name]_gui.png");  // Put your own gui image here

    public $[name]Screen($[name]Container container, PlayerInventory inv, ITextComponent name) {
        super(container, inv, name);
    }

    @Override
    public void render(int mouseX, int mouseY, float partialTicks) {
        this.renderBackground();
        super.render(mouseX, mouseY, partialTicks);
        this.renderHoveredToolTip(mouseX, mouseY);
    }

    @Override
    protected void drawGuiContainerForegroundLayer(int mouseX, int mouseY) {
        // Draw whatever extra information you want here
    }

    @Override
    protected void drawGuiContainerBackgroundLayer(float partialTicks, int mouseX, int mouseY) {
        GlStateManager.color4f(1.0F, 1.0F, 1.0F, 1.0F);
        this.minecraft.getTextureManager().bindTexture(GUI);
        int relX = (this.width - this.xSize) / 2;
        int relY = (this.height - this.ySize) / 2;
        this.blit(relX, relY, 0, 0, this.xSize, this.ySize);
    }
}
/*
====== Code to move to your client initialization ======

        ScreenManager.registerFactory($U{name}_CONTAINER, ${name}Screen::new);

*/
'''
TEMPLATE_BLOCKSTATE_JSON = '''
{
    "variants": {
        "": {
            "model": "$[modid]:block/$L[name]"
        }
    }
}
'''
TEMPLATE_BLOCKMODEL_JSON = '''
{
    "parent": "block/cube_all",
    "textures": {
        "all": "$[modid]:block/$L[name]"
    }
}
'''
TEMPLATE_ITEMMODEL_JSON = '''
{
    "parent": "$[modid]:block/$L[name]"
}
'''
TEMPLATE_LOOTTABLE_JSON = '''
{
  "type": "minecraft:block",
  "pools": [
    {
      "rolls": 1,
      "entries": [
        {
          "type": "minecraft:item",
          "name": "$[modid]:$L[name]"
        }
      ],
      "conditions": [
        {
          "condition": "minecraft:survives_explosion"
        }
      ]
    }
  ]
}
'''
TEMPLATE_RECIPE_JSON = '''
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
#################################################################################
def generate(template: str, inputs: Dict[str, str], conditionals: Dict[str, bool] = {}) -> Dict[str, Any]:
    for cond_name, conditional in conditionals.items():
        lines = template.splitlines()
        gen = True
        newlines = []
        for line in lines:
            if line.strip() == '?{' + cond_name:
                gen = conditional
            elif line.strip() == '?}' + cond_name:
                gen = True
            elif gen:
                newlines.append(line)

        template = '\n'.join(newlines)

    for inp, val in inputs.items():
        template = template.replace(f"$[{inp}]", val)
        template = template.replace(f"$U[{inp}]", val.upper())
        template = template.replace(f"$L[{inp}]", val.lower())
    return template.strip()

def add_templated_java(package: str, name: str, suffix: str, force: bool, template: str, conditionals: Dict[str, bool] = {}):
    path = SOURCE_ROOT
    for folder in package.split('.'):
        path = path.joinpath(folder)
    path.mkdir(parents=True, exist_ok=True)
    java_path = path.joinpath(f"{name}{suffix}.java")

    if (not force) and java_path.exists():
        print(f"File `{java_path}` already exists. Not generated")
    else:
        print(f"Generated `{java_path}`")
        with open(java_path, 'w') as outfile:
            outfile.write(generate(template=template, inputs={
                'package': f"{ROOT_PACKAGE}.{package}",
                'modid_ref': MODID_REF,
                'modid': MODID,
                'name': name
            }, conditionals=conditionals))

def add_templated_json(path: Path, package: str, name: str, force: bool, template: str):
    for folder in package.split('.'):
        path = path.joinpath(folder)
    path.mkdir(parents=True, exist_ok=True)
    json_path = path.joinpath(f"{name.lower()}.json")

    if (not force) and json_path.exists():
        print(f"File `{json_path}` already exists. Not generated")
    else:
        print(f"Generated `{json_path}`")
        with open(json_path, 'w') as outfile:
            json.dump(json.loads(generate(template=template, inputs={
                "modid": MODID,
                "name": name
            })), outfile, indent=2, sort_keys=True)

def add_block(name: str, force: bool, gui: bool, tile: bool, no_json: bool):
    conditionals = {
        'gui': gui,
        'tile': tile
    }
    add_templated_java(package=PACKAGE_BLOCKS, name=name, suffix='Block', force=force, template=TEMPLATE_BLOCK_JAVA, conditionals=conditionals)
    if gui:
        add_templated_java(package=PACKAGE_CONTAINERS, name=name, suffix='Container', force=force, template=TEMPLATE_CONTAINER_JAVA, conditionals=conditionals)
        add_templated_java(package=PACKAGE_SCREENS, name=name, suffix='Screen', force=force, template=TEMPLATE_SCREEN_JAVA, conditionals=conditionals)
    if tile:
        add_templated_java(package=PACKAGE_TILES, name=name, suffix='Tile', force=force, template=TEMPLATE_TILE_JAVA, conditionals=conditionals)
    if not no_json:
        add_templated_json(path = ASSET_RESOURCE_ROOT, package='blockstates', name=name, force=force, template=TEMPLATE_BLOCKSTATE_JSON)
        add_templated_json(path = ASSET_RESOURCE_ROOT, package='models.block', name=name, force=force, template=TEMPLATE_BLOCKMODEL_JSON)
        add_templated_json(path=ASSET_RESOURCE_ROOT, package='models.item', name=name, force=force, template=TEMPLATE_ITEMMODEL_JSON)
        add_templated_json(path=DATA_RESOURCE_ROOT, package='loot_tables.blocks', name=name, force=force, template=TEMPLATE_LOOTTABLE_JSON)
        add_templated_json(path=DATA_RESOURCE_ROOT, package='recipes', name=name, force=force, template=TEMPLATE_RECIPE_JSON)

if __name__ == '__main__':
    parser = ArgumentParser(description='Make a Block')
    parser.add_argument('name', help='CamelCase name of the block to add')
    parser.add_argument('--force', help='Overwrite files even if they exist (be careful!)', action='store_true')
    parser.add_argument('--tile', help='Generate additional code for a tileentity', action='store_true')
    parser.add_argument('--gui', help='Generate additional code for container and gui (implies tile!)', action='store_true')
    parser.add_argument('--nojson', help='Prevent generating json', action='store_true')
    args = parser.parse_args()

    print(f'Adding block {args.name}')
    add_block(name=args.name, force=args.force, gui=args.gui, tile=args.gui or args.tile, no_json=args.nojson)