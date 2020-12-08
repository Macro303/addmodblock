TEMPLATE_SCREEN = '''
package $[package];

import com.mojang.blaze3d.matrix.MatrixStack;
import net.minecraft.client.gui.screen.inventory.ContainerScreen;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.text.ITextComponent;
import org.lwjgl.opengl.GL11;

public class $[name]Screen extends ContainerScreen<$[name]Container> {
    private ResourceLocation background = new ResourceLocation($[modid_ref], "textures/gui/$L[name].png");

    public $[name]Screen($[name]Container container, PlayerInventory inv, ITextComponent title) {
        super(container, inv, title);
    }

    @Override
    public void render(MatrixStack stack, int mouseX, int mouseY, float partialTicks) {
        this.renderBackground(stack);
        super.render(stack, mouseX, mouseY, partialTicks);
        this.renderHoveredToolTip(stack, mouseX, mouseY);
    }

    @Override
    public void init(){
        super.init();
    }

    @Override
    protected void drawGuiContainerForegroundLayer(MatrixStack stack, int mouseX, int mouseY) {
        // Draw whatever extra information you want here
    }

    @Override
    protected void drawGuiContainerBackgroundLayer(MatrixStack stack, float partialTicks, int mouseX, int mouseY) {
        GL11.glColor4f(1, 1, 1, 1);
		getMinecraft().getTextureManager().bindTexture(background);
		this.blit(stack, guiLeft, guiTop, 0, 0, xSize, ySize);
    }
}
/*
====== Code to move to your client initialization ======
        ScreenManager.registerFactory($U[name]_CONTAINER.get(), $[name]Screen::new);
*/
'''