# 1. 导入随机数模块，用于生成随机数字（新手：要实现随机功能，先导入这个模块）
import random

def guess_number_game():
    """猜数字小游戏：猜1-10之间的随机数"""
    # 2. 生成1-10之间的随机整数（作为答案）
    secret_number = random.randint(1, 10)
    # 3. 打印游戏欢迎语
    print("🎉 欢迎来到猜数字小游戏！")
    print("我已经生成了一个1-10之间的数字，快来猜猜看吧！\n")
    
    # 4. 循环猜数字（直到猜对为止）
    while True:
        # 5. 获取用户输入（转换成整数）
        try:
            user_guess = int(input("请输入你猜的数字（1-10）："))
        except ValueError:
            print("❌ 错误：请输入有效的数字！")
            continue
        
        # 6. 条件判断：对比用户输入和答案，给出提示
        if user_guess < 1 or user_guess > 10:
            print("⚠️ 提示：数字超出范围，请输入1-10之间的数字！")
        elif user_guess < secret_number:
            print("⬆️  提示：猜小了，再试大一点的数字！")
        elif user_guess > secret_number:
            print("⬇️  提示：猜大了，再试小一点的数字！")
        else:
            # 7. 猜对了，跳出循环，结束游戏
            print(f"🎉 恭喜你！猜对了！答案就是{secret_number}！")
            break

# 8. 运行游戏
if __name__ == "__main__":
    guess_number_game()