from typing import List

class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        for i in range(len(nums)):
            nums[i] *= nums[i]
        nums.sort()
        return nums

def main():
    # 示例输入
    test_case = [-4, -3, 2, 1]
    solver = Solution()
    result = solver.sortedSquares(test_case)
    print("排序后的平方数组:", result)

if __name__ == "__main__":
    main()