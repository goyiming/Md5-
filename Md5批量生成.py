import tkinter as tk
from tkinter import ttk
import hashlib
from pypinyin import pinyin, Style
from unidecode import unidecode

fixed_chars = "@1234567"
convert_options = None

def convert_to_pinyin():
    hanzi_text = hanzi_entry.get("1.0", "end-1c").strip()
    convert_option = convert_options.get()  # 获取用户选择的转换方式

    if hanzi_text:
        lines = hanzi_text.split('\n')
        pinyin_result = ''
        for line in lines:
            pinyin_text = pinyin(line, style=Style.NORMAL)
            processed_pinyin = ''
            for index, word in enumerate(pinyin_text):
                if convert_option == "全大写":
                    processed_pinyin += word[0].upper()
                elif convert_option == "首字母大写":
                    processed_pinyin += word[0].capitalize() if index == 0 else word[0]
                else:
                    processed_pinyin += word[0].lower()
            processed_pinyin = unidecode(processed_pinyin)
            pinyin_result += processed_pinyin + '\n'

        pinyin_entry.delete("1.0", tk.END)
        pinyin_entry.insert("1.0", pinyin_result)

        update_line_count(None, pinyin_entry, pinyin_line_count_label)  # 更新行数统计

def encrypt_name():
    name = hanzi_entry.get("1.0", "end-1c").strip()
    pinyin_name = pinyin_entry.get("1.0", "end-1c").strip()

    if not pinyin_name:
        convert_to_pinyin()
        pinyin_name = pinyin_entry.get("1.0", "end-1c").strip()

    encrypted_names = ''
    lines = pinyin_name.split('\n')
    for line in lines:
        encrypted_name = hashlib.md5((line + fixed_chars).encode()).hexdigest()
        encrypted_names += encrypted_name + '\n'

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, encrypted_names)

    update_line_count(None, result_text, jieguo_line_count_label)  # 更新行数统计

# 更新行数统计
def update_line_count(event, text_widget, label_widget):
    lines = text_widget.get("1.0", "end-1c").split("\n")
    line_count = len([line for line in lines if line.strip()])
    label_widget.config(text=f"行数统计：{line_count}")

def right_click_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="复制", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="粘贴", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_command(label="剪切", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="全选", command=lambda: widget.tag_add("sel", "1.0", "end"))
    menu.add_command(label="清空", command=lambda: widget.delete("1.0", tk.END))
    widget.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))

# 创建主窗口
root = tk.Tk()
root.title("MD5加密工具")
root.geometry("930x450")

# 设置窗口图标
#root.iconbitmap('xxx')

# 设置固定窗口大小
root.resizable(width=False, height=False)

# 计算屏幕居中的位置
window_width = 930
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width - window_width) / 2)
y_cordinate = int((screen_height - window_height) / 2)

# 设置窗口位置在屏幕中居中显示
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# 创建底部红色文字标签
bottom_label = tk.Label(root, text="o<) 软件说明：根据输入汉字转换成首字母大写拼音，加入固定字符，通过md5形式进行加密得到结果。", fg="red", font=("Arial", 14, "bold"))
bottom_label.grid(row=3, column=0, columnspan=3, sticky="ew")

# 左侧汉字输入框
hanzi_frame = ttk.LabelFrame(root, text="汉字")
hanzi_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
hanzi_entry = tk.Text(hanzi_frame, height=20, width=40)
hanzi_entry.pack(fill=tk.BOTH, expand=True)
hanzi_line_count_label = ttk.Label(hanzi_frame, text="行数统计：0")
hanzi_line_count_label.pack(side=tk.BOTTOM)
hanzi_entry.bind("<KeyRelease>", lambda event: update_line_count(event, hanzi_entry, hanzi_line_count_label))
right_click_menu(hanzi_entry)

# 中间拼音输入框
pinyin_frame = ttk.LabelFrame(root, text="拼音")
pinyin_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
pinyin_entry = tk.Text(pinyin_frame, height=20, width=40)
pinyin_entry.pack(fill=tk.BOTH, expand=True)
pinyin_line_count_label = ttk.Label(pinyin_frame, text="行数统计：0")
pinyin_line_count_label.pack(side=tk.BOTTOM)
pinyin_entry.bind("<KeyRelease>", lambda event: update_line_count(event, pinyin_entry, pinyin_line_count_label))
right_click_menu(pinyin_entry)

# 右侧转换结果显示框
result_frame = ttk.LabelFrame(root, text="转换结果")
result_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
result_text = tk.Text(result_frame, height=20, width=40)
result_text.pack(fill=tk.BOTH, expand=True)
right_click_menu(result_text)
jieguo_line_count_label = ttk.Label(result_frame, text="行数统计：0")
jieguo_line_count_label.pack(side=tk.BOTTOM)

# 固定字符设置区域
fixed_chars_frame = ttk.LabelFrame(root, text="基础设置")
fixed_chars_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

# 创建下拉选择框标签
convert_label = ttk.Label(fixed_chars_frame, text="转换拼音方法：")
convert_label.pack(side=tk.LEFT, padx=4)

# 创建下拉选择框
convert_options = ttk.Combobox(fixed_chars_frame, values=["首字母大写", "全大写", "全小写"])
convert_options.current(0)  # 设置默认选中第一个选项
convert_options.pack(side=tk.LEFT, padx=4)

convert_label = ttk.Label(fixed_chars_frame, text="固定字符设置：")
convert_label.pack(side=tk.LEFT, padx=4)


# 创建固定字符输入框
fixed_chars_entry = ttk.Entry(fixed_chars_frame, width=20)
fixed_chars_entry.insert(0, fixed_chars)
fixed_chars_entry.pack(side=tk.LEFT)

def update_fixed_chars():
    global fixed_chars
    fixed_chars = fixed_chars_entry.get()

fixed_chars_button = ttk.Button(fixed_chars_frame, text="更新固定字符", command=update_fixed_chars)
fixed_chars_button.pack(side=tk.LEFT, padx=5)


# 按钮
button_frame = ttk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=3, pady=5)
# 转换按钮
convert_button = tk.Button(button_frame, text="转换", command=convert_to_pinyin)
convert_button.pack(side=tk.LEFT, padx=4)

# 加密按钮
encrypt_button = tk.Button(button_frame, text="加密", command=encrypt_name)
encrypt_button.pack(side=tk.LEFT, padx=4)

def convert_to_uppercase():
    result_text_uppercase = result_text.get("1.0", "end-1c").strip().upper()
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, result_text_uppercase)

# 结果转大写按钮
uppercase_button = tk.Button(button_frame, text="结果转大写", command=convert_to_uppercase)
uppercase_button.pack(side=tk.LEFT, padx=4)

# 运行主循环
root.mainloop()
