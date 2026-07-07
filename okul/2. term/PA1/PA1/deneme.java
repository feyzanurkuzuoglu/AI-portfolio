import java.time.temporal.ChronoUnit;

public class deneme {
    public static void main(String[] args) {
        LocalDate date1 = LocalDate.of(2024, 3, 1);  // 1 Mart 2024
        LocalDate date2 = LocalDate.of(2024, 3, 19); 


        ChronoUnit.DAYS.between(date1,date2);

    }


import java.util.Scanner;

    public class DateDifferenceCalculator {
    
        public static void main(String[] args) {
            Scanner scanner = new Scanner(System.in);
    
            // Kullanıcıdan iki tarih al
            System.out.print("İlk tarihi (gg/aa/yyyy) formatında giriniz: ");
            String date1 = scanner.nextLine();
    
            System.out.print("İkinci tarihi (gg/aa/yyyy) formatında giriniz: ");
            String date2 = scanner.nextLine();
    
            // Gün farkını hesapla
            int daysBetween = calculateDateDifference(date1, date2);
    
            // Sonucu yazdır
            System.out.println("İki tarih arasındaki gün farkı: " + Math.abs(daysBetween));
    
            scanner.close();
        }
    
        // İki tarih arasındaki farkı hesaplayan fonksiyon
        public static int calculateDateDifference(String date1, String date2) {
            // Gün, ay ve yılı ayrıştır
            int[] d1 = parseDate(date1);
            int[] d2 = parseDate(date2);
    
            // İki tarih için toplam gün sayısını hesapla
            int totalDays1 = totalDays(d1[2], d1[1], d1[0]);
            int totalDays2 = totalDays(d2[2], d2[1], d2[0]);
    
            // Gün farkını döndür
            return totalDays2 - totalDays1;
        }
    
        // "dd/MM/yyyy" formatındaki tarihi gün, ay ve yıl olarak ayıran fonksiyon
        public static int[] parseDate(String date) {
            String[] parts = date.split("/");
            int day = Integer.parseInt(parts[0]);
            int month = Integer.parseInt(parts[1]);
            int year = Integer.parseInt(parts[2]);
            return new int[]{day, month, year};
        }
    
        // Belirtilen tarihe kadar geçen toplam gün sayısını hesaplayan fonksiyon
        public static int totalDays(int year, int month, int day) {
            int totalDays = 0;
    
            // Önceki yılları toplama ekle
            for (int y = 0; y < year; y++) {
                totalDays += isLeapYear(y) ? 366 : 365;
            }
    
            // İçinde bulunulan yılın önceki aylarının toplam günleri
            for (int m = 1; m < month; m++) {
                totalDays += daysInMonth(m, year);
            }
    
            // O ayın içindeki günleri ekle
            totalDays += day;
    
            return totalDays;
        }
    
        // Artık yıl olup olmadığını kontrol eden fonksiyon
        public static boolean isLeapYear(int year) {
            return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
        }
    
        // Ayın kaç gün olduğunu döndüren fonksiyon
        public static int daysInMonth(int month, int year) {
            switch (month) {
                case 1: case 3: case 5: case 7: case 8: case 10: case 12: return 31;
                case 4: case 6: case 9: case 11: return 30;
                case 2: return isLeapYear(year) ? 29 : 28;
                default: return 0; // Geçersiz ay
            }
        }
    }
    
}


    /* 
    
    public void displayItem(LibraryItem item) {
        //addItem(item);
        for (int i = 0; i < itemCount; i++) {
            if (items[i].getId().equals(item.getId())) {
                writeToOutput(items[i].getItemInfo());
                return;
            }
        }
        writeToOutput("Item with ID " + item.getId() + " not found.");
    }



    
    
  
    
    public void displayUser(User user) {
        //addUser(user);
        
        for (int i = 0; i < userCount; i++) {
            if (users[i].getId().equals(user.getId())) {
                writeToOutput(users[i].getUserInfo());
                return;
            }
        }
        writeToOutput("User with ID " + user.getId() + " not found.");

    }

    
    */




