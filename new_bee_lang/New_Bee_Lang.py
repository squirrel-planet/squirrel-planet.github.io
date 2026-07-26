import sys
import random
import io
from typing import List

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding = 'utf-8')

def print_msg(string):
    if '--only-output' not in sys.argv:
        print(string)

def error(message_list: list) -> None:
    if message_list:

        def get_content(value, level = 0):
            content = ''
            for s in value:
                if isinstance(s, str):
                    content += f'\n{level * '  '}·{s}'
                else:
                    content += get_content(s, level + 1)
            return content

        content = get_content(message_list)
        print(f'\n\033[31m{content}\033[0m\n')
    sys.exit(1)

class bee(object):
    def __init__(self, type: str = 'egg', value: str | int | None = None):
        self.type = type
        self.value = value
        self.is_slack = False

    def grow_up(self) -> None:
        if self.type == 'egg':
            self.type = 'young bee'
        else:
            self.type = 'bee'

class new_bee_lang_interpreter(object):
    def __init__(self, code: str):
        self.line_number = 0
        self.code = code
        self.hello = False
        self.goodbye = False
        self.honeycomb_stack: None | List[bee] = None
        self.workspace_stack: List[bee] = []
        self.sky_stack: List[bee] = []
        self.next_bee_value: str | int | None = None
        self.judgment_value: List[bool] = []
        self.loop_break: List[bool] = []
        self.input_value = ''
        self.do_not_give_up: int = 0
        self.do_not_slack: int = 0
        self.honey = 5
        self.encouragements = [
            '继续加油！你快要理解了... 才怪！',
            '哇！你又执行了一条指令！真是个天才！',
            '你知道吗？你正在成为 New Bee Lang 专家的道路上... 走向深渊。',
            '你的代码正在运行，虽然结果是错误的。',
            '如果疼痛是学习的一部分，你现在已经是博士了。',
            '蜜蜂们为你的坚持感到骄傲（真的吗？）。',
            '你确定你想继续吗？还没有人能完整写出这个程序呢。',
            '这个错误是为你特别准备的！',
            '你的咖啡还够吗？因为你会需要很多。',
            '有时候我怀疑你是不是故意的。'
        ]
        self.mocking_messages = {
            'syntax': [
                '这代码比我奶奶的食谱还难懂！',
                '如果代码能哭，它现在正在嚎啕大哭。',
                '这不只是错误，这是对编程艺术的侮辱！',
                '你的键盘是不是被蜜蜂蜇过？',
                '这语法错误气得蜜蜂都想蜇你。',
                '蜜蜂筑巢都比你的代码有条理。',
                '你的代码烂到蜜蜂都不愿意采蜜。',
                '蜜蜂都比你懂得怎么组织代码。',
                '你的代码像只无头蜜蜂乱撞。'
            ],
            'runtime': [
                '/runtime_error: 你的人生选择正在受到质疑/',
                '这只蜜蜂迷路了，就像你的代码逻辑一样。',
                '错误 404：你的代码逻辑未找到。',
                '这不是 bug，这是你代码的特色。',
                '蜜蜂表示你的代码没救了',
                '蜜蜂迷路了，因为你的错误信息比花丛还乱。',
                '这只蜜蜂说：你的代码比它的翅膀还脆弱。',
                '错误：蜜蜂采蜜回来发现你的程序已经崩了。',
                '连蜜蜂都知道怎么处理异常，你不知道？'
            ]
        }

    def get_random_encouragement(self) -> str:
        return random.choice(self.encouragements)

    def get_random_mocking(self, error_type = 'syntax') -> str:
        return random.choice(self.mocking_messages[error_type])

    def error_with_details(
            self, message_list: list,
            operation: str | None = None,
            char: str | None = None,
            error_type = 'runtime') -> None:
        full_message: list = [self.get_random_mocking(error_type)]
        for msg in message_list:
            full_message.append(msg)
        if char:
            insults = [
                f'你在干什么？！字符 “{char}” 不允许使用！',
                f'你脑子里有蜜蜂吗？“{char}” 不是有效的 New Bee Lang 字符！',
                f'我没想到有人会笨到使用 “{char}”，但你做到了！',
                f'“{char}” 这个字符不属于我们的语言！你完了！'
            ]
            full_message.append(random.choice(insults))
            full_message.append(['有效字符: 字母 数字 空格 运算符 (字符值、注释除外)'])
            full_message.append([f'你使用的: “{char}” (真是个天才选择呢)'])
        position = self.line_number
        if position:
            full_message.append([f'位置: 第 {position} 行'])
        if operation:
            full_message.append([f'操作: {operation}'])
            if 'init honeycomb' not in operation:
                if isinstance(self.honeycomb_stack, list):
                    full_message.append([f'当前蜂巢深度: {len(self.honeycomb_stack)}'])
        full_message.append(self.get_random_encouragement())
        error(['错误', full_message, '程序执行失败，蜜蜂们表示遗憾（并没有）'])

    def parse_tokens(self, instruction: str) -> List[str]:
        tokens = []
        current_token = ''
        in_quotes = False
        i = 0
        while i < len(instruction):
            char = instruction[i]
            if char == "'":
                if in_quotes:
                    backslash_count = 0
                    j = i - 1
                    while j >= 0 and instruction[j] == '\\':
                        backslash_count += 1
                        j -= 1
                    if backslash_count % 2 == 1:
                        current_token += "'"
                    else:
                        tokens.append("'" + current_token + "'")
                        current_token = ''
                        in_quotes = False
                else:
                    if current_token:
                        tokens.append(current_token)
                    current_token = ''
                    in_quotes = True
            elif char == ' ' and not in_quotes:
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
            else:
                current_token += char
            i += 1
        if current_token:
            tokens.append(current_token)
        return tokens

    def run(self) -> None:
        lines: List[str] = self.code.split('\n')
        tokens = []
        non_please_count, please_count = (0, 0)
        for line in lines:
            if not line:
                continue
            if line.strip().startswith('#'):
                continue
            in_quotes = False
            i = 0
            while i < len(line):
                char = line[i]
                if char == "'":
                    if in_quotes:
                        backslash_count = 0
                        j = i - 1
                        while j >= 0 and line[j] == '\\':
                            backslash_count += 1
                            j -= 1
                        if backslash_count % 2 == 0:
                            in_quotes = False
                    else:
                        in_quotes = True
                elif not in_quotes and char not in '#0123456789abcdefghijklmnopqrstuvwxyzNBL +-*/"\'\n\t\\':
                    self.error_with_details(
                        [f'字符 "{char}" 不允许使用'],
                        char=char,
                        error_type='syntax'
                    )
                i += 1
            tokens.append(self.parse_tokens(line))
            if tokens[-1][0] == 'please':
                please_count += 1
                non_please_count += 1
            else:
                non_please_count = 0
                if non_please_count >= 5:
                    self.error_with_details([
                        '蜜蜂们放弃了！',
                        '每5句代码必须加一个 please 语句！',
                        '蜜蜂们不喜欢偷懒的程序员！'
                    ], error_type = 'syntax')
        if not tokens:
            self.error_with_details([
                '这个文件里居然没有一个有效代码！',
                '蜜蜂们生气了！'
            ])
        please_ratio = float(please_count) / len(tokens)
        if not (0.4 <= please_ratio <= 0.5):
            self.error_with_details([
                'please 语句占比不正确！',
                f'当前 please 占比: {please_ratio * 100:.1f}%',
                '要求: 40% ~ 50%',
                '蜜蜂们不喜欢不守规矩的程序员！'
            ], error_type = 'syntax')
        for line_tokens in tokens:
            if line_tokens[0] == 'loop':
                if len(line_tokens) > 2:
                    if line_tokens[1] == 'end' and self.loop_break[-1]:
                        self.loop_break.pop()
                        continue
            self.run_line(line_tokens)
        if not self.goodbye:
            self.error_with_details([
                '你没有告别！程序必须以 goodbye New Bee Lang 结尾！',
                '这是 New Bee Lang 的基本礼仪！',
                '没有告别，蜜蜂们会伤心的！',
                '请在你的代码结尾添加: goodbye New Bee Lang',
                'P.S. 蜜蜂们期待你的下次光临（并不）！'
            ])
        if self.judgment_value or self.loop_break:
            self.error_with_details(['你的 loop 或 judgment 没有结束！蜜蜂气得把你蛰得嗷嗷叫。'])

    def too_long_code_error(self, tokens: List[str], all_tokens: List[str]) -> None:
        self.error_with_details([
            '语句执行完还有多余的代码？看来蜂蜜很喜欢这种代码（真的吗）！',
            f'快把多余的 {' '.join(tokens)} 删除！'
        ], ' '.join(all_tokens))

    def too_short_code_error(self, cmd) -> None:
        self.error_with_details([f'命令 {cmd} 后的参数不够！蜂蜜气急败坏，直接报错！'], cmd)

    def uninit_error(self, cmd) -> None:
        self.error_with_details(
            ['你没有初始化蜂巢！', f'没有蜂巢，怎么使用 {cmd} 命令？', '快点添加 init honeycomb 命令！'],
            operation = cmd
        )

    def bee_error(self, cmd: str, bee_type: str = 'worker bee') -> None:
        self.error_with_details([f'工作区的正在工作蜂不是 {bee_type}，怎么执行 {cmd} 命令？'], cmd)

    def not_have_start_error(self, cmd: str) -> None:
        self.error_with_details([f'你没有执行 {cmd} start 命令！怎么就执行 {cmd} end 了？！'], cmd)

    def slack_error(self, cmd: str) -> None:
        self.error_with_details(['蜂蜜正在偷懒，快使用 do not slack 命令让它工作！'], cmd)

    def honeycomb_end(self, cmd: str | None = None) -> bee:
        if self.honeycomb_stack is None:
            if cmd:
                self.uninit_error(cmd)
        elif self.honeycomb_stack:
            return self.honeycomb_stack[-1]
        else:
            self.error_with_details(['看来某人正在操作空蜂巢呢！'])
        return bee()

    def input(self) -> str | int:
        if not self.input_value:
            self.input_value = input()
        first = self.input_value[0]
        if first.isdigit():
            i = 0
            while i < len(self.input_value) and self.input_value[i].isdigit():
                i += 1
            result = int(self.input_value[:i])
            self.input_value = self.input_value[i:]
            return result
        else:
            self.input_value = self.input_value[1:]
            return first

    def give_up(self):
        print_msg('\n程序结束。再见，愚蠢的人类！蜜蜂们要去采蜜了。')
        sys.exit(0)

    def is_working_bee_slack(self) -> bool:
        return self.workspace_stack[-1].is_slack

    def has_queen_bee(self, stack: List[bee], exclude: bee | None = None) -> bool:
        for b in stack:
            if b.type == 'queen bee' and b is not exclude:
                return True
        return False

    def has_alive_queen_elsewhere(self, exclude: bee | None = None) -> bool:
        stacks = []
        if self.honeycomb_stack is not None:
            stacks.append(self.honeycomb_stack)
        stacks.append(self.workspace_stack)
        stacks.append(self.sky_stack)
        for stack in stacks:
            if self.has_queen_bee(stack, exclude):
                return True
        return False

    def run_line(self, tokens: List[str]) -> None:
        self.line_number += 1
        if not tokens:
            return
        if tokens == ['please']:
            self.error_with_details(['看来只说 please 而不说事的人蜂蜜是永远不会理他的呢！'], 'please')
        if tokens[0] == 'please':
            tokens = tokens[1:]
        cmd = tokens[0]
        length = len(tokens)
        if cmd == 'hello':
            if tokens[1:] != ['New', 'Bee', 'Lang']:
                self.error_with_details([
                    'hello 后面只能是 New Bee Lang！'
                ])
            if self.hello:
                self.error_with_details([
                    '你已经打了招呼！不能多次打招呼！',
                    '一只蜂蜜心想：这个程序员真啰嗦！我偷偷报个错，不过分吧！'
                ])
            self.hello = True
        elif self.hello:
            if cmd == 'loop':
                if self.judgment_value:
                    if not self.judgment_value[-1]:
                        return
                if length > 2:
                    self.too_long_code_error(tokens[2:], tokens)
                elif length < 2:
                    self.too_short_code_error('loop')
                elif self.workspace_stack[-1].type != 'worker bee':
                    self.bee_error('worker bee')
                elif self.is_working_bee_slack():
                    self.slack_error('loop')
                else:
                    if tokens[1] == 'start':
                        self.loop_break.append(False)
                    elif tokens[1] == 'end' and self.loop_break[-1]:
                        self.loop_break.pop()
                        return
            if cmd == 'judgment':
                if self.loop_break:
                    if self.loop_break[-1]:
                        return
                if length < 2:
                    self.too_short_code_error('judgment')
                elif self.workspace_stack[-1].type != 'worker bee':
                    self.bee_error('judgment')
                elif self.is_working_bee_slack():
                    self.slack_error('judgment')
                elif self.honeycomb_stack is None:
                    self.uninit_error('judgment')
                elif tokens[1] == 'start':
                    if length > 2:
                        self.too_long_code_error(tokens[2:], tokens)
                    val = self.honeycomb_end('judgment start').value
                    if val is not None and val != '0' and val != 0:
                        self.judgment_value.append(True)
                    else:
                        self.judgment_value.append(False)
                elif tokens[1] in ['<', '>', '<=', '>=', '==', '!=']:
                    if length < 3:
                        self.too_short_code_error('judgment')
                    elif length > 3:
                        self.too_long_code_error(tokens[3:], tokens)
                    elif tokens[2] != 'start':
                        self.error_with_details([f'judgment 语法错误！'], 'judgment')
                    elif len(self.honeycomb_stack) < 2:
                        self.error_with_details(
                            ['蜂巢中的蜜蜂数量不足以进行比较运算！'],
                            f'judgment {tokens[1]}'
                        )
                    else:
                        op = tokens[1]
                        bee1, bee2 = self.honeycomb_stack[-2], self.honeycomb_stack[-1]
                        value1, value2 = bee1.value, bee2.value
                        if not isinstance(value1, int) or not isinstance(value2, int):
                            self.error_with_details(
                                ['只有数字才能参与比较运算！'],
                                f'judgment {op}'
                            )
                        exp = f'{value1} {op} {value2}'
                        result = eval(exp)
                        self.judgment_value.append(bool(result))
                elif tokens[1] == 'end':
                    if not self.judgment_value:
                        self.not_have_start_error('judgment')
                    else:
                        self.judgment_value.pop()
                        return
                else:
                    self.error_with_details([f'judgment 无法进行 {tokens[1]} 操作！'], 'judgment')
            if self.loop_break:
                if self.loop_break[-1]:
                    return
            if self.judgment_value:
                if not self.judgment_value[-1]:
                    return
            if cmd == 'goodbye':
                if tokens[1:] != ['New', 'Bee', 'Lang']:
                    self.error_with_details(
                        ['goodbye 后面只能是 New Bee Lang！']
                    )
                if self.goodbye:
                    self.error_with_details([
                        '你已经说了再见！不能多次说再见！',
                        '一只蜂蜜心想：这个程序员真啰嗦！我偷偷报个错，不过分吧！'
                    ])
                self.goodbye = True
            elif cmd == 'init':
                if length > 1 and tokens[1:][0] == 'honeycomb':
                    if isinstance(self.honeycomb_stack, list):
                        self.error_with_details(
                            ['这已经是一个完整的蜂巢了！不能初始化！'],
                            operation = 'init honeycomb'
                        )
                    self.honeycomb_stack = [bee('queen bee')]
                else:
                    self.too_short_code_error('init')
                if length > 2:
                    self.too_long_code_error(tokens[2:], tokens)
            elif cmd == 'call':
                if self.honeycomb_stack is not None:
                    if len(self.honeycomb_stack) == 0:
                        self.error_with_details(
                            ['蜂巢里没有蜜蜂！你没法使用 call 命令！'],
                            operation = 'call'
                        )
                    bee_to_call = self.honeycomb_end('call')
                    if bee_to_call.type == 'egg':
                        self.error_with_details(
                            ['egg 不能 call！', '卵都还没孵化呢，怎么叫它干活？'],
                            operation = 'call'
                        )
                    if bee_to_call.type == 'young bee':
                        self.error_with_details(
                            ['young bee 不能 call！', '羽翼未丰，叫来也干不了活！'],
                            operation = 'call'
                        )
                    if bee_to_call.type == 'queen bee' and self.has_queen_bee(self.workspace_stack):
                        self.error_with_details(
                            ['冲突！一个工作区不能有多个 queen bee！'],
                            operation = 'call'
                        )
                    self.workspace_stack.append(bee_to_call)
                    self.honeycomb_stack = self.honeycomb_stack[0:-1]
                else:
                    self.uninit_error('call')
                if length >= 2:
                    self.too_long_code_error(tokens[1:], tokens)
            elif cmd == 'lay':
                if length > 2:
                    self.too_long_code_error(tokens[2:], tokens)
                elif length < 2:
                    self.too_short_code_error('lay')
                if tokens[1] != 'egg':
                    self.error_with_details([
                        '你想要干什么？！只能使用 lay egg 命令来控制 queen bee 产卵！',
                        f'你是想产 {tokens[1]} 吗？！',
                        '快改回 lay egg 命令！'
                    ])
                if self.honeycomb_stack is None:
                    self.uninit_error('lay egg')
                elif self.workspace_stack[-1].type == 'queen bee':
                    if not self.honey:
                        self.error_with_details(['没有蜂蜜了！后悔没有使用 get honey 命令吧！'], 'lay egg')
                    bee_value_first = self.next_bee_value
                    self.next_bee_value = None
                    self.honeycomb_stack.append(bee('egg', bee_value_first))
                    self.honey -= 1
                elif self.is_working_bee_slack():
                    self.slack_error('lay egg')
                else:
                    self.bee_error('lay egg', 'queen bee')
            elif cmd == 'sleep':
                if self.honeycomb_stack is not None:
                    if self.honeycomb_end('sleep').type == 'egg':
                        self.honeycomb_stack[-1].grow_up()
                    else:
                        self.error_with_details([f'{self.honeycomb_stack[-1].type} 不能睡觉！'], 'sleep')
                else:
                    self.uninit_error('sleep')
                if length > 1:
                    self.too_long_code_error(tokens[1:], tokens)
            elif cmd == 'eat':
                if self.honeycomb_stack is not None:
                    if self.honeycomb_end('eat').type == 'young bee':
                        self.honeycomb_stack[-1].grow_up()
                        self.honey -= 1
                    else:
                        self.error_with_details([f'{self.honeycomb_stack[-1].type} 不能吃蜂蜜！'], 'eat')
                else:
                    self.uninit_error('sleep')
                if length > 1:
                    self.too_long_code_error(tokens[1:], tokens)
            elif cmd == 'give':
                if length > 2:
                    self.too_long_code_error(tokens[2:], tokens)
                elif length < 2:
                    self.too_short_code_error('give')
                elif tokens[1] == 'up':
                    self.give_up()
                else:
                    self.error_with_details(['你连退出命令都不会？！快点改为 give up 指令！'], 'give')
            elif cmd == 'get':
                if length > 2:
                    self.too_long_code_error(tokens[2:], tokens)
                elif length < 2:
                    self.too_short_code_error('get')
                elif tokens[1] != 'honey':
                    self.error_with_details([f'无法获取 {tokens[1]}！'], f'get {tokens[1]}')
                elif self.workspace_stack[-1].type != 'worker bee':
                    self.bee_error('get honey')
                elif self.is_working_bee_slack():
                    self.slack_error('get honey')
                else:
                    self.honey += 1
            elif cmd == 'input':
                if length > 1:
                    self.too_long_code_error(tokens[1:], tokens)
                self.next_bee_value = self.input()
            elif cmd == 'random':
                if length > 1:
                    self.too_long_code_error(tokens[1:], tokens)
                self.next_bee_value = random.randint(0, 9)
            elif cmd == 'set':
                if length > 4 and tokens[1] == 'type':
                    self.too_long_code_error(tokens[4:], tokens)
                elif length > 3  and tokens[1] != 'type':
                    self.too_long_code_error(tokens[3:], tokens)
                elif length < 3:
                    self.too_short_code_error(cmd)
                if self.honeycomb_stack is None:
                    self.uninit_error('set')
                elif tokens[1] == 'type':
                    if self.honeycomb_stack[-1].type in ['queen bee', 'young bee', 'egg']:
                        self.error_with_details(
                            ['queen bee 、young bee 或 egg 不能设置 type！'], 'set type'
                        )
                    if self.honeycomb_stack[-1].value is not None and tokens[2:] == ['worker', 'bee']:
                        self.error_with_details(['有值的蜂蜜不能设置 type 为 worker bee 类型！'], 'set type')
                    if tokens[2:] == ['queen', 'bee']:
                        if self.has_queen_bee(self.honeycomb_stack, self.honeycomb_stack[-1]):
                            self.error_with_details(
                                ['冲突！一个蜂巢不能有多个 queen bee！'], 'set type'
                            )
                        self.honeycomb_stack[-1].type = 'queen bee'
                    elif tokens[2:] in [['bee'], ['worker', 'bee']]:
                        self.honeycomb_stack[-1].type = ' '.join(tokens[2:])
                    else:
                        self.error_with_details([f'你不能设置 {' '.join(tokens[2:])} 这个 type'], 'set type')
                elif tokens[1] == 'value':
                    if self.workspace_stack[-1].type != 'worker bee':
                        self.bee_error('set value')
                    elif self.is_working_bee_slack():
                        self.slack_error('set value')
                    raw = tokens[2]
                    value = None
                    parsed = None
                    if raw == 'random':
                        value = random.randint(0, 9)
                    else:
                        try:
                            parsed = eval(raw)
                        except:
                            self.error_with_details(['设置的值不正确'], f"set value {raw}")
                        if isinstance(parsed, int):
                            value = parsed
                        elif isinstance(parsed, str) and len(parsed) >= 1:
                            value = parsed
                        else:
                            self.error_with_details(['设置的值不正确'], f"set value {raw}")
                    if self.honeycomb_stack:
                        self.honeycomb_stack[-1].value = value
                    else:
                        self.error_with_details(['蜂巢是空的'], f"set value s{raw}")
            elif cmd == 'output':
                if length > 1:
                    self.too_long_code_error(tokens[1:], tokens)
                if self.workspace_stack[-1].type != 'worker bee':
                    self.bee_error('output')
                elif self.is_working_bee_slack():
                    self.slack_error('output')
                output_value = self.honeycomb_end('output').value
                if output_value is None:
                    self.error_with_details(['你没有设置值，无法输出！'], 'output')
                print(output_value, end = '')
            elif cmd == 'go':
                if length > 1:
                    if tokens[1] == 'back':
                        if self.honeycomb_stack is None:
                            self.uninit_error('go back')
                        else:
                            if self.workspace_stack[-1].type == 'queen bee' and self.has_queen_bee(self.honeycomb_stack):
                                self.error_with_details(
                                    ['冲突！一个蜂巢不能有多个 queen bee！'],
                                    'go back'
                                )
                            self.honeycomb_stack.append(self.workspace_stack[-1])
                            self.workspace_stack = self.workspace_stack[:-1]
                    else:
                        self.error_with_details([f'你想去 {tokens[1]} ？不可能！'], f'go {tokens[1]}')
                else:
                    self.too_short_code_error('go')
                if length > 2:
                    self.too_long_code_error(tokens[2:], tokens)
            elif cmd == 'fly':
                if length > 2:
                    self.too_long_code_error(tokens[2:], tokens)
                elif length == 2:
                    if tokens[1] == 'back':
                        if self.honeycomb_stack is None:
                            self.uninit_error('fly back')
                        elif not self.sky_stack:
                            self.error_with_details(['天空中一只蜜蜂都没有！无法 fly back！'], 'fly back')
                        else:
                            if self.sky_stack[-1].type == 'queen bee' and self.has_queen_bee(self.honeycomb_stack):
                                self.error_with_details(
                                    ['冲突！一个蜂巢不能有多个 queen bee！'],
                                    'fly back'
                                )
                            self.honeycomb_stack.append(self.sky_stack[-1])
                            self.sky_stack = self.sky_stack[:-1]
                    else:
                        self.error_with_details([f'你想飞 {tokens[1]}？不可能！'], f'fly {tokens[1]}')
                else:
                    if self.honeycomb_stack is None:
                        self.uninit_error('fly')
                    elif not self.honeycomb_stack:
                        self.error_with_details(['蜂巢里没有蜜蜂！无法 fly！'], 'fly')
                    else:
                        bee_to_fly = self.honeycomb_end('fly')
                        if bee_to_fly.type == 'egg':
                            self.error_with_details(
                                ['egg 不能 fly！', '连翅膀都没长出来呢，飞什么飞？'],
                                operation = 'fly'
                            )
                        elif bee_to_fly.type == 'young bee':
                            self.error_with_details(
                                ['young bee 不能 fly！', '羽翼未丰，想飞还早着呢！'],
                                operation = 'fly'
                            )
                        if bee_to_fly.type == 'queen bee' and self.has_queen_bee(self.sky_stack):
                            self.error_with_details(
                                ['冲突！天空中不能有多个 queen bee！'],
                                'fly'
                            )
                        self.sky_stack.append(bee_to_fly)
                        self.honeycomb_stack = self.honeycomb_stack[:-1]
            elif cmd == 'kill':
                if self.honeycomb_stack is None:
                    self.uninit_error('kill')
                elif self.honeycomb_end('kill').type == 'queen bee':
                    this_bee = self.honeycomb_stack[-1]
                    if self.has_alive_queen_elsewhere(this_bee):
                        self.honeycomb_stack.pop()
                    else:
                        self.error_with_details([
                            '所有 queen bee 都驾崩了！',
                            '蜂后驾崩，王朝终结！',
                            '这就像你的代码生涯一样，尚未开始就已结束。'
                        ], 'kill')
                else:
                    self.honeycomb_stack.pop()
            elif cmd == 'all':
                if self.honeycomb_stack is None:
                    self.uninit_error('all')
                elif length > 2:
                    self.too_long_code_error(tokens[2:], tokens)
                elif length == 2:
                    thing = tokens[1]
                    if thing == 'kill':
                        while self.honeycomb_stack:
                            this_bee = self.honeycomb_stack.pop()
                            if this_bee.type == 'queen bee':
                                if not self.has_alive_queen_elsewhere():
                                    self.error_with_details([
                                        '所有 queen bee 都驾崩了！',
                                        '蜂后驾崩，王朝终结！',
                                        '这就像你的代码生涯一样，尚未开始就已结束。'
                                    ], 'all kill')
                    else:
                        self.error_with_details([f'没人知道 {thing} 是什么命令，蜂蜜们同样如此。'])
                else:
                    self.too_short_code_error('all')
            elif cmd == 'compute':
                if self.workspace_stack[-1].type != 'worker bee':
                    self.bee_error('compute')
                elif self.is_working_bee_slack():
                    self.slack_error('compute')
                if self.honeycomb_stack is None:
                    self.uninit_error('compute')
                elif length > 2:
                    self.too_long_code_error(tokens[1:], tokens)
                elif length < 2:
                    self.too_short_code_error('compute')
                else:
                    op = tokens[1]
                    bee1, bee2 = self.honeycomb_stack[-2], self.honeycomb_stack[-1]
                    value1, value2 = bee1.value, bee2.value
                    if op not in ['+', '-', '*', '/']:
                        self.error_with_details([f'“{op} 是什么运算符？！”蜂蜜大喊道。'], f'compute {op}')
                    if not isinstance(value1, int) or not isinstance(value2, int):
                        self.error_with_details(
                            ['只有数字才能参与运算！', '字符类型的蜜蜂不能做算术！'],
                            f'compute {op}'
                        )
                    if value2 == 0 and op == '/':
                        self.error_with_details(['你想毁灭世界吗？！居然除以 0！'], 'compute /')
                    exp = f'{value1} {op} {value2}'
                    try:
                        self.next_bee_value = eval(exp)
                    except Exception:
                        self.error_with_details(
                            ['看来计算出错了！蜜蜂们感同身受（难道你信吗？）！'],
                            f' {op}'
                        )
            elif cmd == 'do':
                if length > 3 and tokens[2] != 'give':
                    self.too_long_code_error(tokens[3:], tokens)
                elif length > 4 and tokens[2] == 'give':
                    self.too_long_code_error(tokens[4:], tokens)
                elif tokens[1] != 'not':
                    self.error_with_details(
                        [
                            f'语法不正确！do {tokens[1]} 命令把井井有条的蜂蜜队列破坏了！',
                            '看来蜜蜂们要来报仇了！'
                        ], f'do {tokens[1]}'
                    )
                else:
                    things_not_to_do = tokens[2:]
                    if things_not_to_do == ['give', 'up']:
                        self.do_not_give_up = 5
                    elif things_not_to_do == ['slack']:
                        self.do_not_slack = 5
            elif cmd == 'error':
                if length > 1:
                    self.too_long_code_error(tokens[1:], tokens)
                error_list = []
                if self.honeycomb_stack is None:
                    self.uninit_error('error')
                else:
                    for this_bee in self.honeycomb_stack:
                        if this_bee.value != None:
                            error_list.append(this_bee.value)
                        else:
                            self.error_with_details(['蜂巢内有的蜂蜜没有值，无法报错'])
                    error([''.join(error_list), '这是你要求的！'])
            else:
                self.error_with_details(
                    [f'命令 {' '.join(tokens)} 是什么意思！？蜜蜂不语，只是一味的报错'],
                    ' '.join(tokens)
                )
        else:
            self.error_with_details([
                '你没有打招呼！程序必须以 hello New Bee Lang 开头！',
                '这是 New Bee Lang 的基本礼仪！',
                '没有问候，就没有代码运行!',
                '请在你的代码开头添加: hello New Bee Lang',
                'P.S. 蜜蜂们不会欢迎粗鲁的程序员！'
            ])
        if cmd != 'hello' and not self.do_not_give_up:
            self.error_with_details(['蜜蜂们放弃了！', '快使用 do not give up 命令！'])
        if not self.do_not_slack:
            if self.workspace_stack:
                self.workspace_stack[-1].is_slack = True
        if self.do_not_slack and self.workspace_stack:
            self.workspace_stack[-1].is_slack = False
        self.do_not_give_up -= 1
        self.do_not_slack -= 1

def main() -> None:
    if len(sys.argv) < 2:
        error(
            ['错误: 没有填入参数', '请使用: python New_Bee_Lang.py <file_name>',
            '示例: python New_Bee_Lang.py hello_world.nbl']
        )
    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding = 'utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        code = ''
        error([f'文件 <{file_path}> 不存在', '蜜蜂们找不到你的代码文件！', '读取文件失败，蜜蜂们表示同情（并没有）'])
    except Exception:
        code = ''
        error(['读取文件失败，蜜蜂们表示同情（并没有）'])
    interpreter = new_bee_lang_interpreter(code)
    interpreter.run()
    print_msg('\n程序结束。再见，愚蠢的人类！蜜蜂们要去采蜜了。')

if __name__ == '__main__':
    main()
