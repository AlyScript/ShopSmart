import compare.test_variables as cmp_tests
import compare.operator as operator

def perform_title_test(test_title_pack):
    titles = [title[0] for title in test_title_pack]
    expected_results = [title[1] for title in test_title_pack]
    passed_tests = 0
    
    print(f"<-**** Title to compare: '{titles[0]}' ****->")
    print("\n")
    
    results = operator.operate_titles(titles)
      
    for i, result in enumerate(results):
        _, title, is_similar, value = result
        if is_similar == expected_results[i]:
            passed_tests += 1
            print(f'Test {i+1} PASS 🟪 "{title}"')
        else:
            if expected_results[i] is True:
                print(f'Test {i+1} FAIL 🟥 --- The similarity between "{titles[0]}" and "{title}" is: {value} ---  ❌: EXP ✅')
            else:
                print(f'Test {i+1} FAIL 🟥 --- The similarity between "{titles[0]}" and "{title}" is: {value} ---  ✅: EXP ❌')
    
    print("\n")
    print(f"----- Test Complete: {passed_tests} out of {len(titles)} tests passed -----")
    
    return

for block in cmp_tests.test_titles:
    print("\n")
    perform_title_test(block)
print("\n")
