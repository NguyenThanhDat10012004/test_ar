import {loadGLTF} from "../../libs/loader.js";
import {mockWithVideo, mockWithImage} from '../../libs/camera-mock.js';
const THREE = window.MINDAR.IMAGE.THREE;

document.addEventListener('DOMContentLoaded', () => {
  const start = async() => {

    // 1. GỌI MOCK NGAY LẬP TỨC
    // Giờ đây hàm navigator.mediaDevices.getUserMedia đã bị ghi đè
    // (Đảm bảo bạn chạy Live Server và dùng đường dẫn tương đối)
    console.log("BẮT ĐẦU MOCK CAMERA");
    // mockWithImage('../../assets/targets/anchor.jpg');

    // // 2. TẠO MINDAR
    // const mindarThree = new window.MINDAR.IMAGE.MindARThree({
    //   container: document.body,
    //   imageTargetSrc: '../../assets/targets/targets.mind',
    // });
    // mockWithVideo('../../assets/mock-videos/musicband1.mp4');
    
    console.log("TẠO MINDAR");
    const mindarThree = new window.MINDAR.IMAGE.MindARThree({
      container: document.body,
      imageTargetSrc: './targets.mind',
    });
    const {renderer, scene, camera} = mindarThree;

    // 3. THÊM ÁNH SÁNG
    const light = new THREE.HemisphereLight( 0xffffff, 0xbbbbff, 1 );
    scene.add(light);

    // 4. TẢI MODEL (Sau khi đã sửa lỗi CSP)
    try {
      const raccoon = await loadGLTF('https://nguyenthanhdat10012004.github.io/anki_ar/data/travel/beach.glb');
      console.log("RACCOON:", raccoon);
      raccoon.scene.scale.set(0.1, 0.1, 0.1);
      raccoon.scene.position.set(0, 1, 0);

      const anchor = mindarThree.addAnchor(0);
      anchor.group.add(raccoon.scene);
    } catch (err) {
      console.error("LỖI TẢI MODEL:", err);
    }
    console.log("MODEL ĐÃ ĐƯỢC THÊM VÀO SCENE");
    // 5. START MINDAR
    // Bây giờ, khi start() gọi getUserMedia, nó sẽ gọi hàm mock của bạn
    await mindarThree.start();
    console.log("MINDAR ĐÃ KHỞI ĐỘNG");
    // 6. CHẠY RENDER LOOP
    renderer.setAnimationLoop(() => {
      renderer.render(scene, camera);
    });
    console.log("BẮT ĐẦU RENDER LOOP");
  }
  start();
});