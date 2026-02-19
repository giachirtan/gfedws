from collections import deque, Counter
from datetime import datetime

# Danh sách phòng
ROOMS_FULL = {
    'nk': 'Nhà kho',
    'ph': 'Phòng họp',
    'pgd': 'Phòng giám đốc',
    'ptc': 'Phòng trò chuyện',
    'pgs': 'Phòng giám sát',
    'vp': 'Văn phòng',
    'ptv': 'Phòng tài vụ',
    'pns': 'Phòng nhân sự'
}

class SatThuTool:
    def __init__(self):
        self.history = deque(maxlen=10)   # tự động giữ đúng 10 ván
        self.last_room = None

    def them_phong(self, room_code):
        room_code = room_code.lower().strip()
        if room_code not in ROOMS_FULL:
            print("❌ Mã phòng sai! Các mã hợp lệ:", ", ".join(ROOMS_FULL.keys()))
            return

        print(f"\n{'═' * 70}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sát thủ vừa vào → {room_code.upper()} - {ROOMS_FULL[room_code]}")

        # Kiểm tra streak
        if self.last_room is not None:
            if room_code == self.last_room:
                print("🔴 SÁT THỦ VÀO LẠI PHÒNG CŨ → TOOL NGỪNG ĐẶT, CHỈ QUAN SÁT!")
                print("   (Chờ sát thủ di chuyển phòng mới rồi mới theo)")
            else:
                print(f"🟢 Sát thủ DI CHUYỂN sang phòng MỚI!")
                print(f"✅ ĐỀ XUẤT: VÀO NGAY PHÒNG {ROOMS_FULL[room_code].upper()} cho ván tiếp theo!")

        # Cập nhật lịch sử
        self.history.append(room_code)
        self.last_room = room_code

        # Luôn hiển thị lịch sử + tần suất
        self.hien_thi_lich_su()

        # Chỉ khi KHÔNG streak mới dự đoán
        if self.last_room != room_code or len(self.history) == 1:  # lần đầu hoặc di chuyển mới
            self.du_doan_va_de_xuat()

    def hien_thi_lich_su(self):
        print(f"\n📜 LỊCH SỬ 10 VÁN GẦN NHẤT ({len(self.history)}/10):")
        for i, room in enumerate(reversed(list(self.history)), 1):
            print(f"   {i:2d}. {room.upper():<4} → {ROOMS_FULL[room]}")

        print("\n📊 TẦN SUẤT:")
        count = Counter(self.history)
        for room in ROOMS_FULL.keys():
            freq = count.get(room, 0)
            percent = freq / len(self.history) * 100 if self.history else 0
            bar = "█" * freq
            print(f"   {room.upper():<4} : {freq:2d} lần ({percent:4.1f}%) {bar}")

    def du_doan_va_de_xuat(self):
        if len(self.history) < 2:
            return

        current = self.last_room

        # Dự đoán phòng tiếp theo (transition từ phòng hiện tại)
        transitions = Counter()
        for i in range(len(self.history) - 1):
            if self.history[i] == current:
                transitions[self.history[i + 1]] += 1

        if transitions:
            next_room = transitions.most_common(1)[0][0]
        else:
            # fallback
            next_room = Counter(self.history).most_common(1)[0][0]

        # Phòng an toàn nhất (ít vào nhất)
        count = Counter(self.history)
        safest = min(count, key=count.get) if count else 'nk'

        print(f"\n🎯 DỰ ĐOÁN CHO VÁN TIẾP THEO:")
        print(f"   🔥 Phòng sát thủ hay vào nhất : {next_room.upper()} - {ROOMS_FULL[next_room]}")
        print(f"   🛡️  Phòng AN TOÀN NHẤT        : {safest.upper()} - {ROOMS_FULL[safest]}")

    def reset(self):
        self.history.clear()
        self.last_room = None
        print("✅ Đã reset toàn bộ lịch sử!")


# ====================== CHẠY TOOL ======================
if __name__ == "__main__":
    print("🔪 TOOL DỰ ĐOÁN PHÒNG SÁT THỦ - Bản tự động hoá theo cơ chế bạn yêu cầu 🔪\n")
    print("Hướng dẫn: Nhập mã phòng sát thủ vừa vào (nk, ph, pgd, ptc, pgs, vp, ptv, pns)")
    print("Lệnh đặc biệt: reset | exit\n")

    tool = SatThuTool()

    while True:
        try:
            inp = input("\n➤ Sát thủ vừa vào phòng: ").strip()
            if inp.lower() in ['exit', 'thoát', 'q']:
                print("Cảm ơn bạn đã dùng tool! Chúc bạn thắng nhiều ván nhé ❤️")
                break
            elif inp.lower() == 'reset':
                tool.reset()
                continue
            tool.them_phong(inp)
        except KeyboardInterrupt:
            print("\n\nTool đã dừng.")
            break