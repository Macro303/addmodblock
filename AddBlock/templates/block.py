TEMPLATE_BLOCK = '''
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
====== Code to move to your registration event class ======

public static RegistryObject<$[name]Block> $U[name] = BLOCKS.register("$L[name]", $[name]Block::new);
public static RegistryObject<BlockItem> $U[name]_BLOCKITEM = ITEMS.register("$L[name]", () -> new BlockItem($U[name].get(), new Properties()));
*/
'''