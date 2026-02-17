  // Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.7.0/firebase-app.js";
import { getFirestore, doc, getDoc } from "https://www.gstatic.com/firebasejs/12.7.0/firebase-firestore.js";
import { collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/12.7.0/firebase-firestore.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBXgv9x9NFT67QXgssNLB41aDQACMusZwE",
  authDomain: "unlock-key-smte.firebaseapp.com",
  projectId: "unlock-key-smte",
  storageBucket: "unlock-key-smte.firebasestorage.app",
  messagingSenderId: "725579747736",
  appId: "1:725579747736:web:9f24fc28dca1157eea1bed",
  measurementId: "G-BLF7BEQZWY"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);




let num=document.getElementById("seenum")
for (let i=1;i<=30;i++) {
    const option=document.createElement("option")
    option.value=i
    option.textContent=i
    num.appendChild(option)
}
//  p'pk
console.log(29689);
let bt=document.getElementById("btsubmit");


const form = document.querySelector("form");


form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const selectedNum = num.value;             

    const { value: text } = await Swal.fire({
        title: "กรุณากรอกรหัส",
        input: "text",
        inputLabel: "Input Password",
        inputPlaceholder: "กรอกรหัสที่นี่",
        inputAttributes: {
            maxlength: "20",
            autocapitalize: "off",
            autocorrect: "off"
        },
        showCancelButton: true
    });

    if (text === undefined) return;

    if (!selectedNum) {
        Swal.fire("แจ้งเตือน", "กรุณาเลือกเลขที่ก่อน", "warning");
        return;
    }

    Swal.fire({
        title: "Loading",
        text: "กำลังโหลด กรุณารอสักครู่",
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    setTimeout(async () => {
    Swal.close();

    const ref = doc(db, "passwords", selectedNum);
    const snap = await getDoc(ref);

    if (snap.exists() && text === snap.data().pass) {
        Swal.fire({
            icon: "success",
            title: "✅ Correct!",
            html: `
              <p>รหัสที่คุณกรอกคือ</p>
              <b style="font-size:18px;color:green;">${text}</b>
              <p>โปรดแคปภาพหน้าจอหน้านี้ เพื่อเป็นหลักฐาน</p>`
        });
    } else {
        Swal.fire({
            icon: "error",
            title: "❌ Wrong password",
            html: `
              <p>รหัสที่คุณกรอกคือ</p>
              <b style="font-size:18px;color:red;">${text}</b>
              <p>กรุณาลองใหม่</p>`
        });
    }
    await addDoc(collection(db, "logs"), {
    number: selectedNum,
    input: text,
    result: snap.exists() && text === snap.data().pass ? "correct" : "wrong",
    time: serverTimestamp()
    });
    }, 1700);


});