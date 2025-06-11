// DOMの全要素が読み込まれた後に実行されるイベントリスナーを追加
document.addEventListener('DOMContentLoaded', function(){
    
    // 現在時刻を取得して更新する関数
    function updateTime(){
        // 現在の日時を取得
        const now = new Date();

        // 年、月、日、時、分、秒をそれぞれ取得し、2桁表示に整形
        const year = now.getFullYear(); // 年を取得
        const month = (now.getMonth() + 1).toString().padStart(2,'0'); // 月を取得し、0から始まるので+1(1月は0なので＋1する)、2桁表示する（一桁の時は0で埋める　tostringは文字列に変換）
        const day = now.getDate().toString().padStart(2,'0'); // 日を取得し、2桁表示
        const hours = now.getHours().toString().padStart(2,'0'); // 時を取得し、2桁表示
        const minutes = now.getMinutes().toString().padStart(2,'0'); // 分を取得し、2桁表示
        const seconds = now.getSeconds().toString().padStart(2,'0'); // 秒を取得し、2桁表示

        // 日付のフォーマットを指定して文字列を作成
        const dateString = `${year}年${month}月${day}日`;
        // 時刻のフォーマットを指定して文字列を作成
        const timeString = `${hours}時${minutes}分${seconds}秒`;
        // 日付と時刻を結合した文字列を作成
        const dateTimeString = `${dateString} ${timeString}`;

        // HTML内の要素（IDが'clock'の要素）に作成した日時の文字列を表示
        document.getElementById('clock').textContent = dateTimeString;
    }

    // ページが読み込まれたときに最初に時刻を表示
    updateTime();
    // 1秒ごとにupdateTime関数を呼び出して、時刻を更新
    setInterval(updateTime, 1000); // 1000ms (1秒)ごとに時刻を更新
});
