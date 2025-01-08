import os
import tkinter as tk
from tkinter import messagebox
from data_manager import save_data, load_data, list_files

def format_currency(value):
    """숫자를 3자리마다 콤마로 포맷"""
    try:
        value = value.replace(",", "")  # 기존 입력에서 콤마 제거
        formatted = "{:,.0f}".format(float(value))  # 포맷 적용
        return formatted
    except ValueError:
        return value  # 숫자가 아니면 그대로 반환

def on_total_amount_change(event):
    """총 자산 금액 입력 필드에 콤마 표시 및 커서 위치 유지"""
    value = total_amount_entry.get()
    if value:
        cursor_position = total_amount_entry.index(tk.INSERT)
        raw_value = value.replace(",", "")  # 기존 입력값에서 콤마 제거
        prev_length = len(value)
        formatted_value = format_currency(raw_value)
        new_length = len(formatted_value)

        total_amount_entry.delete(0, tk.END)
        total_amount_entry.insert(0, formatted_value)

        new_cursor_position = cursor_position + (new_length - prev_length)
        if new_cursor_position < 0:
            new_cursor_position = 0
        total_amount_entry.icursor(new_cursor_position)

def save_current_data():
    """현재 데이터를 JSON 파일로 저장"""
    try:
        title = portfolio_title_entry.get()
        if not title:
            raise ValueError("포트폴리오 제목을 입력하세요.")

        total_amount = total_amount_entry.get()
        if not total_amount:
            raise ValueError("총 자산 금액을 입력하세요.")

        try:
            total_amount = int(total_amount.replace(",", ""))
        except ValueError:
            raise ValueError("올바른 금액을 입력하세요.")

        assets = []
        for frame in asset_frames:
            asset_name = frame["name"].get()
            asset_percent = frame["percent"].get()
            if asset_name and asset_percent:
                try:
                    asset_percent = float(asset_percent)
                    assets.append({"name": asset_name, "percent": asset_percent})
                except ValueError:
                    raise ValueError(f"{asset_name}의 비율이 올바르지 않습니다.")

        filename = f"{title}.json"
        data = {"total_amount": total_amount, "assets": assets}
        save_data(filename, data)
        refresh_file_list()
    except Exception as e:
        messagebox.showerror("오류", str(e))

def load_selected_data(filename):
    """선택된 파일의 데이터를 로드"""
    try:
        data = load_data(filename)
        portfolio_title_entry.delete(0, tk.END)
        portfolio_title_entry.insert(0, filename.replace(".json", ""))

        total_amount_entry.delete(0, tk.END)
        total_amount_entry.insert(0, f"{data['total_amount']:,}")

        for frame in asset_frames:
            frame["frame"].destroy()
        asset_frames.clear()

        for asset in data["assets"]:
            add_asset_field(asset["name"], str(asset["percent"]))
    except Exception as e:
        messagebox.showerror("로드 오류", str(e))

def refresh_file_list():
    """JSON 파일 목록을 갱신"""
    try:
        file_listbox.delete(0, tk.END)
        for filename in list_files():
            file_listbox.insert(tk.END, filename)
    except Exception as e:
        messagebox.showerror("목록 갱신 오류", str(e))

def on_file_select(event):
    """파일 선택 시 자동 로드"""
    try:
        selection = event.widget.curselection()
        if selection:
            filename = event.widget.get(selection[0])
            load_selected_data(filename)
    except Exception as e:
        messagebox.showerror("파일 선택 오류", str(e))

def add_asset_field(name="", percent=""):
    """새로운 자산 입력 필드 추가"""
    try:
        frame = tk.Frame(asset_frame)
        frame.pack(pady=5)

        tk.Label(frame, text="자산 이름:").pack(side="left")
        name_entry = tk.Entry(frame, width=15)
        name_entry.insert(0, name)
        name_entry.pack(side="left", padx=5)

        tk.Label(frame, text="비율(%):").pack(side="left")
        percent_entry = tk.Entry(frame, width=10)
        percent_entry.insert(0, percent)
        percent_entry.pack(side="left", padx=5)

        asset_frames.append({"frame": frame, "name": name_entry, "percent": percent_entry})
    except Exception as e:
        messagebox.showerror("자산 추가 오류", str(e))

def reset_portfolio():
    """새로운 포트폴리오 작성을 위해 입력 필드를 초기화"""
    try:
        portfolio_title_entry.delete(0, tk.END)
        total_amount_entry.delete(0, tk.END)
        for frame in asset_frames:
            frame["frame"].destroy()
        asset_frames.clear()
    except Exception as e:
        messagebox.showerror("초기화 오류", str(e))

def delete_selected_file():
    """선택된 파일 삭제"""
    try:
        selection = file_listbox.curselection()
        if not selection:
            raise ValueError("삭제할 파일을 선택하세요.")

        filename = file_listbox.get(selection[0])
        filepath = os.path.join("data", filename)

        if os.path.exists(filepath):
            os.remove(filepath)

        # 목록에서 제거
        refresh_file_list()
    except Exception as e:
        messagebox.showerror("삭제 오류", str(e))

def calculate_rebalance():
    """리밸런싱 계산 및 결과 출력"""
    try:
        total_amount = total_amount_entry.get()
        if not total_amount:
            raise ValueError("총 자산 금액을 입력하세요.")

        try:
            total_amount = int(total_amount.replace(",", ""))
        except ValueError:
            raise ValueError("올바른 금액을 입력하세요.")

        assets = []
        for frame in asset_frames:
            asset_name = frame["name"].get()
            asset_percent = frame["percent"].get()
            if asset_name and asset_percent:
                try:
                    asset_percent = float(asset_percent)
                    assets.append({"name": asset_name, "percent": asset_percent})
                except ValueError:
                    raise ValueError(f"{asset_name}의 비율이 올바르지 않습니다.")

        total_percent = sum(asset["percent"] for asset in assets)
        if total_percent != 100:
            raise ValueError("자산 비율의 합이 100%가 아닙니다.")

        results = []
        for asset in assets:
            target_amount = total_amount * (asset["percent"] / 100)
            results.append(f"{asset['name']}: {format_currency(str(target_amount))}원")

        result_label.config(text="\n".join(results))
    except Exception as e:
        messagebox.showerror("오류", str(e))

# GUI 설정
root = tk.Tk()
root.title("리밸런싱 프로그램")
root.geometry("800x600")

# 왼쪽 파일 목록
file_list_frame = tk.Frame(root)
file_list_frame.pack(side="left", fill="y", padx=10, pady=10)
tk.Label(file_list_frame, text="저장된 데이터").pack()
file_listbox = tk.Listbox(file_list_frame, width=30, height=20)
file_listbox.pack(fill="y")
file_listbox.bind("<<ListboxSelect>>", on_file_select)

add_portfolio_button = tk.Button(file_list_frame, text="+", command=reset_portfolio, width=5, height=2)
add_portfolio_button.pack(pady=5)

delete_file_button = tk.Button(file_list_frame, text="삭제", command=delete_selected_file, width=5, height=2)
delete_file_button.pack(pady=5)

# 오른쪽 입력 섹션
main_frame = tk.Frame(root)
main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(main_frame, text="포트폴리오 제목:").pack(pady=5)
portfolio_title_entry = tk.Entry(main_frame)
portfolio_title_entry.pack()

tk.Label(main_frame, text="총 자산 금액:").pack(pady=10)
total_amount_entry = tk.Entry(main_frame)
total_amount_entry.pack()
total_amount_entry.bind("<KeyRelease>", on_total_amount_change)

tk.Label(main_frame, text="자산 이름과 비율 입력:").pack(pady=10)
asset_frame = tk.Frame(main_frame)
asset_frame.pack()

asset_frames = []
tk.Button(main_frame, text="자산 추가", command=lambda: add_asset_field()).pack(pady=5)
tk.Button(main_frame, text="데이터 저장", command=save_current_data).pack(pady=5)
tk.Button(main_frame, text="리밸런싱 계산", command=calculate_rebalance).pack(pady=5)

result_label = tk.Label(main_frame, text="", justify="left", anchor="w")
result_label.pack(pady=10)

refresh_file_list()
root.mainloop()
