import collections

# Danh sách 8 phòng
ROOMS = {
    'nk': 'Nhà kho',
    'ph': 'Phòng họp',
    'pgd': 'Phòng giám đốc',
    'ptc': 'Phòng trò chuyện',
    'pgs': 'Phòng giám sát',
    'vp': 'Văn phòng',
    'ptv': 'Phòng tài vụ',
    'pns': 'Phòng nhân sự'
}

class SatThuPredictor:
    def __init__(self):
        self.history = [] # Lưu trữ lịch sử (tối đa 10 ván)

    def add_round(self, room_code):
        if room_code not in ROOMS:
            print("❌ Mã phòng không hợp lệ! Vui lòng nhập lại.")
            return False
        
        self.history.append(room_code)
        # Chỉ giữ lại lịch sử 10 ván gần nhất
        if len(self.history) > 10:
            self.history.pop(0)
        return True

    def analyze(self):
        print("\n" + "="*50)
        print(f"📊 LỊCH SỬ {len(self.history)} VÁN GẦN NHẤT:")
        history_names = [ROOMS[code] for code in self.history]
        print(" -> ".join(history_names))
        print("-" * 50)

        # 1. CƠ CHẾ DỰ ĐOÁN & ĐẶT CƯỢC
        if len(self.history) < 2:
            print("⏳ Trạng thái Tool: Đang thu thập dữ liệu (cần ít nhất 2 ván để phân tích).")
            if len(self.history) == 1:
                 print(f"🎯 Gợi ý đặt cược: {ROOMS[self.history[-1]]}")
        else:
            last_room = self.history[-1]
            prev_room = self.history[-2]

            if last_room == prev_room:
                print("🛑 TRẠNG THÁI: NGỪNG ĐẶT VÀ QUAN SÁT")
                print(f"Lý do: Sát thủ đang ở lỳ tại [{ROOMS[last_room]}].")
            else:
                print("✅ TRẠNG THÁI: BẮT ĐẦU VÀO TIỀN")
                print(f"🎯 Phòng dự đoán (Sát thủ có tỉ lệ chọn tiếp theo): [{ROOMS[last_room]}]")

        # 2. ĐỀ XUẤT PHÒNG AN TOÀN NHẤT (Dựa trên 10 ván gần nhất)
        if self.history:
            room_counts = {code: 0 for code in ROOMS}
            for code in self.history:
                room_counts[code] += 1
            
            min_visits = min(room_counts.values())
            safe_rooms = [ROOMS[code] for code, count in room_counts.items() if count == min_visits]
            
            print("-" * 50)
            print(f"🛡️ PHÒNG AN TOÀN NHẤT (Bị vào ít nhất - {min_visits} lần):")
            print(", ".join(safe_rooms))
        print("="*50 + "\n")

def main():
    predictor = SatThuPredictor()
    
    print("=== TOOL DỰ ĐOÁN SÁT THỦ ===")
    print("Danh sách mã phòng để nhập:")
    for code, name in ROOMS.items():
        print(f" - {code}: {name}")
    print("\nNhập 'q' để thoát chương trình.")
    print("============================\n")

    while True:
        user_input = input("Nhập mã phòng sát thủ vừa vào (vd: nk, ph...): ").strip().lower()
        
        if user_input == 'q':
            print("Đã thoát tool. Chúc bạn may mắn!")
            break
        
        if predictor.add_round(user_input):
            predictor.analyze()

if __name__ == "__main__":
    main()