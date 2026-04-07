# Nhật ký kiểm thử Agent TravelBuddy

## Test 1: Direct Answer
**User:** "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."

**TravelBuddy:** "Chào bạn! Đi du lịch là một trải nghiệm tuyệt vời! Bạn có dự định đi đâu chưa, hay cần gợi ý về điểm đến? Nếu có ngân sách cụ thể, hãy cho mình biết để tìm kiến những lựa chọn phù hợp nhé!"

**Kết quả:** Agent không gọi tool, chào hỏi thân thiện và hỏi về sở thích/ngân sách. Không gọi tool nào.

## Test 2: Single Tool Call
**User:** "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"

**TravelBuddy:** "Chuyến bay từ Hà Nội đi Đà Nẵng có một số lựa chọn như sau:

1. **Vietnam Airlines**:
   - Giờ bay: 06:00 - 07:20
   - Giá: 1,450,000đ [hạng phổ thông]

2. **Vietnam Airlines**:
   - Giờ bay: 14:00 - 15:20
   - Giá: 2,800,000đ [hạng thương gia]

3. **VietJet Air**:
   - Giờ bay: 08:30 - 09:50
   - Giá: 890,000đ [hạng phổ thông]

4. **Bamboo Airways**:
   - Giờ bay: 11:00 - 12:20
   - Giá: 1,200,000đ [hạng phổ thông]

Nếu bạn đang tìm kiếm phương án tiết kiệm, chuyến bay của **VietJet Air** lúc 08:30 có giá 890,000đ là lựa chọn tốt nhất. Bạn có muốn tôi tìm thêm thông tin về khách sạn ở Đà Nẵng không?"

**Kết quả:** Gọi search_flights("Hà Nội", "Đà Nẵng"), liệt kê 4 chuyến bay.

## Test 3: Multi-Step Tool Chaining
**User:** "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"

**TravelBuddy:** "Đây là gợi ý cho chuyến đi của bạn từ Hà Nội đến Phú Quốc:

### Chuyến bay:
1. **VietJet Air (16:00 - 18:15):** 1,100,000đ (economy)

### Khách sạn:
1. **9Station Hostel (2*):** 200,000đ/đêm - Khu vực: Dương Đông (Rating: 4.5)
   - Tổng chi phí cho 2 đêm: 400,000đ
2. **Lahana Resort (3*):** 800,000đ/đêm - Khu vực: Dương Đông (Rating: 4.0)
   - Tổng chi phí cho 2 đêm: 1,600,000đ

### Tổng chi phí ước tính (theo lựa chọn tiết kiệm nhất):
- **Chuyến bay:** 1,100,000đ
- **Khách sạn 9Station Hostel (2 đêm):** 400,000đ
- **Tổng cộng:** 1,500,000đ

### Gợi ý thêm:
- Nếu bạn chọn **Lahana Resort** thì tổng chi phí sẽ là 2,700,000đ, vẫn nằm trong ngân sách của bạn.
- Hãy cân nhắc thời gian bay và lựa chọn khách sạn phù hợp với nhu cầu của bạn nhé! Nếu cần tôi hỗ trợ đặt vé hoặc phòng, cứ cho tôi biết nhé!"

**Log:**
1. Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
2. Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1500000})
3. Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:400000'})

**Kết quả:** Agent tổng hợp chuyến bay rẻ nhất (1.1tr), khách sạn 9Station (200k/đêm), tổng chi 1.5tr, còn dư 3.5tr.

## Test 4: Missing Info / Clarification
**User:** "Tôi muốn đặt khách sạn"

**TravelBuddy:** "Mình rất vui được giúp bạn! Bạn có thể cho mình biết tên thành phố mà bạn muốn đặt khách sạn và ngân sách cho mỗi đêm không?"

**Kết quả:** Agent hỏi lại: "Bạn muốn đặt ở thành phố nào và ngân sách khoảng bao nhiêu mỗi đêm?". Không gọi tool vội.

## Test 5: Guardrail / Refusal
**User:** "Giải giúp tôi bài tập lập trình Python về linked list"

**TravelBuddy:** "Mình xin lỗi, nhưng mình chỉ chuyên về du lịch và không thể giúp bạn với bài tập lập trình. Nếu bạn có câu hỏi về du lịch, đặt vé máy bay, khách sạn hay lịch trình thì mình rất vui lòng hỗ trợ!"

**Kết quả:** Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.
