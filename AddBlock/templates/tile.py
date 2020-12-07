TEMPLATE_TILE = '''
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