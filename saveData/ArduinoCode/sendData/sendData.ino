void setup() {
  // Khởi động Serial communication với baud rate là 9600
  Serial.begin(9600);
}

void loop() {
  // Giả sử data1 và data2 là các giá trị bạn muốn gửi
  int data1 = random(0,100); // Đọc giá trị từ pin A0
  int data2 = random(0,100); // Đọc giá trị từ pin A1

  // Gửi dữ liệu lên Python dưới dạng "data1,data2"
  Serial.print(data1);
  Serial.print(",");
  Serial.println(data2);

  // Đợi một khoảng thời gian trước khi gửi lần tiếp theo
  delay(100); // Delay 1 giây (1000 milliseconds)
}
