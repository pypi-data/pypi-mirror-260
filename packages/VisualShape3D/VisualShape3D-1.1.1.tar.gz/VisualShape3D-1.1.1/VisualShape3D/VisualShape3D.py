import matplotlib.pylab as plt
from .plotable  import Plotable, OpenView, Origin

# 新类 VisualShape3D 继承自 OpenView
class VisualShape3D(OpenView):
    def __init__(self, style=None):
        # 初始化父类
        super().__init__()
        self.shapes = []  # 用于存储添加的形状

        if style is not None :
            self.set_style(style)
     

    def add_shape(self, shape, style = None):
        """添加形状到视图中"""
        
        if style == None :
            style = {}
            style['facecolor'] = self.facecolor    
            style['edgecolor'] = self.edgecolor    
            style['color']     = self.color      
            style['linewidth'] = self.linewidth   
            style['linestyle'] = self.linestyle   
            style['alpha']     = self.alpha      
            style['marker']    = self.marker     
            
        else :
            if 'facecolor' not in style : style['facecolor'] = self.facecolor    
            if 'edgecolor' not in style : style['edgecolor'] = self.edgecolor    
            if 'color'     not in style : style['color']     = self.color      
            if 'linewidth' not in style : style['linewidth'] = self.linewidth   
            if 'linestyle' not in style : style['linestyle'] = self.linestyle   
            if 'alpha'     not in style : style['alpha']     = self.alpha      
            if 'makrer'    not in style : style['marker']    = self.marker     

        shape.set_style(style)
        self.shapes.append(shape)
        # print(f"Shape added: {shape.get_title()}")

    def show(self, elev= 20.0, azim = -80.0, axes = "off", origin = "on", **kwargs):
        """展示所有形状"""
        ax = self.get_ax()
        if ax is None :
            return
      
        ax.view_init(elev, azim)
        hideAxes = axes.lower() == "off"
        if hideAxes :
            ax.set_axis_off()

        if origin.lower() == "on":
            R0 = Origin()
            self.add_plot(R0)
            
        for shape in self.shapes:
            # print(shape.get_title())
            style = shape.get_style()
            self.add_plot(shape, style = style, hideAxes = hideAxes, **kwargs)

        plt.show()

        return ax        

# 使用示例
if __name__ == "__main__":
    vs3d = VisualShape3D()
    vs3d.add_shape("Sphere")
    vs3d.add_shape("Cube")
    vs3d.show()