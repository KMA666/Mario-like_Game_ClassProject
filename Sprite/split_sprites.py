# split_sprites.py - 用于预处理精灵表
import pygame
import os
# 修正导入路径
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 延迟导入 sprite_sheet，避免pygame初始化问题
def get_split_function():
    from sprite_sheet import split_sprite_sheet
    return split_sprite_sheet

def main():
    # 初始化pygame，但不创建窗口
    pygame.init()
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查Ninja Frog目录中实际存在哪些文件
    ninja_frog_dir = os.path.join(current_dir, "Main Characters", "Ninja Frog")
    
    print(f"检查目录: {ninja_frog_dir}")
    
    if os.path.exists(ninja_frog_dir):
        files = os.listdir(ninja_frog_dir)
        print("Ninja Frog目录中的文件:")
        for file in files:
            print(f"  - {file}")
        
        # 处理所有PNG文件
        png_files = [f for f in files if f.lower().endswith('.png')]
        
        # 获取分割函数
        split_sprite_sheet = get_split_function()
        
        for sheet_name in png_files:
            sheet_path = os.path.join(ninja_frog_dir, sheet_name)
            if os.path.exists(sheet_path):
                print(f"\n正在处理: {sheet_name}")
                try:
                    # 读取精灵表尺寸
                    sprite_sheet_img = pygame.image.load(sheet_path)
                    sheet_width = sprite_sheet_img.get_width()
                    sheet_height = sprite_sheet_img.get_height()
                    
                    print(f"精灵表尺寸: {sheet_width} x {sheet_height}")
                    
                    # 如果宽度大于高度，很可能是水平排列的动画帧
                    if sheet_width > sheet_height:
                        # 计算可能的帧数，基于已知的精灵宽度
                        possible_widths = [32, 34, 36, 42, 68, 70, 38]
                        
                        for assumed_width in possible_widths:
                            if sheet_width % assumed_width == 0:
                                actual_sprite_width = assumed_width
                                actual_sprite_height = sheet_height
                                print(f"检测到 {sheet_width//actual_sprite_width} 帧动画，精灵尺寸: {actual_sprite_width}x{actual_sprite_height}")
                                
                                # 分割精灵表
                                split_sprite_sheet(sheet_path, actual_sprite_width, actual_sprite_height, ninja_frog_dir)
                                break
                        else:
                            # 如果没有找到匹配的宽度，使用默认值
                            actual_sprite_width = 32
                            actual_sprite_height = sheet_height
                            print(f"使用默认精灵尺寸: {actual_sprite_width}x{actual_sprite_height}")
                            
                            # 分割精灵表
                            split_sprite_sheet(sheet_path, actual_sprite_width, actual_sprite_height, ninja_frog_dir)
                    else:
                        # 如果是正方形或其他形状，使用默认尺寸
                        actual_sprite_width = min(sheet_width, 64)
                        actual_sprite_height = min(sheet_height, 64)
                        
                        # 尝试找到能整除的尺寸
                        for size in [64, 48, 32, 24, 16]:
                            if sheet_width % size == 0 and sheet_height % size == 0:
                                actual_sprite_width = size
                                actual_sprite_height = size
                                break
                        
                        print(f"使用精灵尺寸: {actual_sprite_width}x{actual_sprite_height}")
                        
                        # 分割精灵表
                        split_sprite_sheet(sheet_path, actual_sprite_width, actual_sprite_height, ninja_frog_dir)
                        
                except Exception as e:
                    print(f"处理 {sheet_name} 时出错: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"文件不存在: {sheet_path}")
    else:
        print("Ninja Frog目录不存在!")

if __name__ == "__main__":
    main()