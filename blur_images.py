"""
포트폴리오용 이미지 블러 처리 스크립트

사용법:
  python blur_images.py                    # assets/images/ 하위 전체 블러 처리 (원본 덮어쓰기)
  python blur_images.py --input image.png  # 단일 이미지 처리
  python blur_images.py --strength light   # 블러 강도 조절 (light/medium/heavy)

필요 라이브러리:
  pip install opencv-python
"""

import cv2
import argparse
import os
import glob


BLUR_STRENGTH = {
    "light": (15, 15),
    "medium": (31, 31),
    "heavy": (61, 61),
}


def blur_image(filepath: str, strength: str = "medium"):
    img = cv2.imread(filepath)
    if img is None:
        print(f"[SKIP] 읽을 수 없는 파일: {filepath}")
        return False

    ksize = BLUR_STRENGTH.get(strength, BLUR_STRENGTH["medium"])
    blurred = cv2.GaussianBlur(img, ksize, 0)

    h, w = blurred.shape[:2]
    if w > 1200:
        ratio = 1200 / w
        blurred = cv2.resize(blurred, (1200, int(h * ratio)))

    cv2.imwrite(filepath, blurred, [cv2.IMWRITE_PNG_COMPRESSION, 6])
    print(f"[OK] {filepath}")
    return True


def process_directory(base_dir: str, strength: str = "medium"):
    extensions = ("*.png", "*.jpg", "*.jpeg", "*.bmp")
    count = 0

    for ext in extensions:
        for filepath in glob.glob(os.path.join(base_dir, "**", ext), recursive=True):
            if "profile" in os.path.basename(filepath).lower():
                print(f"[SKIP] 프로필 사진 제외: {filepath}")
                continue
            if blur_image(filepath, strength):
                count += 1

    print(f"\n총 {count}개 이미지 블러 처리 완료")


def main():
    parser = argparse.ArgumentParser(description="포트폴리오용 이미지 블러 처리")
    parser.add_argument("--input", type=str, help="단일 이미지 경로")
    parser.add_argument(
        "--strength",
        type=str,
        default="medium",
        choices=["light", "medium", "heavy"],
        help="블러 강도 (기본값: medium)",
    )
    parser.add_argument(
        "--dir",
        type=str,
        default="assets/images",
        help="처리할 디렉토리 (기본값: assets/images)",
    )

    args = parser.parse_args()

    if args.input:
        blur_image(args.input, args.strength)
    else:
        process_directory(args.dir, args.strength)


if __name__ == "__main__":
    main()
