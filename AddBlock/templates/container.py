TEMPLATE_CONTAINER = '''
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

    public $[name]Container(int windowId, World world, BlockPos pos, PlayerInventory inv, PlayerEntity player) {
        super($U[name]_CONTAINER, windowId);
        tileEntity = world.getTileEntity(pos);
        this.playerEntity = player;

        tileEntity.getCapability(CapabilityItemHandler.ITEM_HANDLER_CAPABILITY).ifPresent(h -> {
            // Add more slots here if needed
            addSlot(new SlotItemHandler(h, 0, 64, 24));
        });
        layoutPlayerInventorySlots(inv, 10, 70);
    }

    @Override
    public boolean canInteractWith(PlayerEntity player) {
        return isWithinUsableDistance(IWorldPosCallable.of(tileEntity.getWorld(), tileEntity.getPos()), playerEntity, $U[name].get());
    }

    private void layoutPlayerInventorySlots(PlayerInventory inv, int leftCol, int topRow) {
        // Player inventory
        int index = 9;
        int y = topRow;
        for (int j = 0; j < 3; j++) {
            int x = leftCol;
            for (int i = 0; i < 9; i++) {
                addSlot(new Slot(inv, index++, x, y));
                x += 18;
            }
            y += 18;
        }

        // Hotbar
        topRow += 58;
        index = 0;
        int x = leftCol;
        for (int i = 0; i < 9; i++) {
            addSlot(new Slot(inv, index++, x, topRow));
            x += 18;
        }
    }

    @Override
    public ItemStack transferStackInSlot(PlayerEntity player, int index) {
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