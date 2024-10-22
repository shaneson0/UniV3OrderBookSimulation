def split_bytes_string(bytes_string):
    # 将bytes string切割成每个bytes32
    bytes32_list = [bytes_string[i:i+64] for i in range(0, len(bytes_string), 64)]
    return bytes32_list

# 示例用法
bytes_string = "fffffffffffffffffffffffffffcc0f2fffffffffffff6611f6a51e0e7cb8645fffffffffffffffffffffffffffcc1ec000000000000fd9a8358fa1800bd98e6fffffffffffffffffffffffffffcc25000000000000050a42f26d524040a5e92fffffffffffffffffffffffffffcc2b40000000000009ae28a17a80175300fabfffffffffffffffffffffffffffcc2e6ffffffffffffc4c6513731e68458f82afffffffffffffffffffffffffffcc476ffffffffffff993de468255358033e0cfffffffffffffffffffffffffffcc4a8fffffffffffec88ca71f2ad7e2b6b89dfffffffffffffffffffffffffffcc570ffffffffffff93cc86d2fd9535283b98fffffffffffffffffffffffffffcc6ceffffffffffff295e8eac9e89b86a7818fffffffffffffffffffffffffffcc732ffffffffffffe9000520c195ccf63817fffffffffffffffffffffffffffcc7c8fffffffffffed71dd9464e22b7e66aa9fffffffffffffffffffffffffffcc7fafffffffffffb7f4252cba4a14a3dcfeefffffffffffffffffffffffffffcc926fffffffffffe2c97b61a4aab4e94e0cbfffffffffffffffffffffffffffcca20ffffffffffff02657ca705e7ff42671afffffffffffffffffffffffffffccab6ffffffffffff147946c182da86c591c3fffffffffffffffffffffffffffccc14ffffffffffffc0eca1bb13f5118c46f0fffffffffffffffffffffffffffcccaaffffffffffff9f18c51537604eceab28fffffffffffffffffffffffffffcced0fffffffffffff930842f0f8a4721a400fffffffffffffffffffffffffffcd0f6ffffffffffffa3eb0c5abe6acff310f9fffffffffffffffffffffffffffcd128ffffffffffffd5d0d4175922a315270cfffffffffffffffffffffffffffcd3e4fffffffffffee779b5ec7d98a4184843fffffffffffffffffffffffffffcd4acfffffffffffff97cd9268dfa7baca23cfffffffffffffffffffffffffffcd5d8ffffffffffff7efa1bdf3293052740c5fffffffffffffffffffffffffffcd66effffffffffdb57aabf5166e54eaa2546fffffffffffffffffffffffffffcd9c0fffffffffffff0cb98009bf0bd922347fffffffffffffffffffffffffffcdb1effffffffffffe755e6223970fabe9585fffffffffffffffffffffffffffcdb82fffffffffffd8f084973589e24c8805bfffffffffffffffffffffffffffcdce0ffffffffffffc2fb1a7c15ec62abf707fffffffffffffffffffffffffffcdd12ffffffffffff7546f06fb2b2ec230360fffffffffffffffffffffffffffce3b6fffffffffffeefe4add36d7ef7110b6afffffffffffffffffffffffffffce79effffffffffffffef7dabb39edef694a1fffffffffffffffffffffffffffd1c8cfffffffffffffeebe4d8cb59cd79c6fb000000000000000000000000000d89d2ffffffffffbd883b35b0ba8de69923cdfffffffffffffffffffffffffffcbf6200000000000480bdad345b5eb5c23012fffffffffffffffffffffffffffcbe04000000000001d36849e5b554b16b1f35fffffffffffffffffffffffffffcbda000000000000006cf7bd0f075b8de5c00fffffffffffffffffffffffffffcbd3cffffffffffff7f7f38fd2fab27f649f5fffffffffffffffffffffffffffcbca600000000000128e226b9b1dd48199557fffffffffffffffffffffffffffcbc42000000000000c7a95682a34c592e16ccfffffffffffffffffffffffffffcbc10000000000000099ee095ae1f183479bbfffffffffffffffffffffffffffcbb7a0000000000003b39aec8ce197ba707d6fffffffffffffffffffffffffffcbae4000000000000d6a171536176479587e8fffffffffffffffffffffffffffcbab20000000000003f135e44ec0aee73b910fffffffffffffffffffffffffffcb9ea00000000000016fffadf3e6a3309c7e9fffffffffffffffffffffffffffcb88c0000000000002a2f2be8a6dd5cead8f4fffffffffffffffffffffffffffcb760000000000001101b522c928108eef496fffffffffffffffffffffffffffcb472ffffffffffceb881b7822510d72ef17dfffffffffffffffffffffffffffcb3aa000000000024a85540ae991ab155dabafffffffffffffffffffffffffffcb34600000000000270f7b68ca761db377fa5fffffffffffffffffffffffffffcb2e20000000000000f3467ff640f426ddcb9fffffffffffffffffffffffffffcb1b600000000000118864a1382675be7b7bdfffffffffffffffffffffffffffcaff40000000000003d04e583ea139d5408f9fffffffffffffffffffffffffffcae00000000000000068326d9720584535dc4fffffffffffffffffffffffffffcabda000000000000ecb4402fd2bfa2e17a73fffffffffffffffffffffffffffca824000000000000001082544c6121096b5ffffffffffffffffffffffffffffca7c000000000000018aa19ddc68f05416a7bfffffffffffffffffffffffffffca6c60000000000008ab90f904d4d13dcfca0fffffffffffffffffffffffffffca3d80000000000008105e420cd6cfad8bf3bfffffffffffffffffffffffffffc9f5afffffffffffffea12e9745ec387749a7fffffffffffffffffffffffffffc9d02000000000001377358e0d5281d494763fffffffffffffffffffffffffffc9aaa0000000000005c14f3a54195300cef07fffffffffffffffffffffffffffc9a14ffffffffffc7855fa9091024694233a3fffffffffffffffffffffffffffc933e000000000000015ed168ba13c788b659fffffffffffffffffffffffffffc701600000000000001141b2734a632863905fffffffffffffffffffffffffffc6bca0000000000387aa056f6efdb96bdcc5dfffffffffffffffffffffffffff2762e000000000073bf4312cd20614237eab6"
result = split_bytes_string(bytes_string)

# 定义一个数组，记录从-887250 ～ 887250的一个DeltaL累加值
deltaL_accumulated = [0] * (887250 - (-887250) + 1)

currenctTick = -212792

liquidity = 146397912183698051832063671

tick_spacing = 50

# 将结果存储在一个列表中
deltaL_datas = []
for item in result:
    tick_number = int(item[:32], 16)
    deltaL = int(item[32:], 16)
    if tick_number >= 2**127:
        tick_number -= 2**128
    if deltaL >= 2**127:
        deltaL -= 2**128
    deltaL_datas.append((tick_number, deltaL))

# 按照tick_number排序
deltaL_datas.sort(key=lambda x: x[0])



