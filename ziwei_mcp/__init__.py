"""
紫微斗数 MCP Server
为 AI 助手（豆包、Claude、ChatGPT 等）提供紫微斗数排盘与运势分析服务。

启动方式：
  # stdio 模式（供 AI 桌面端连接）
  python mcp_server.py

  # HTTP/SSE 模式（部署到 skymans.cn）
  python mcp_server.py --http 0.0.0.0:8000
"""

from __future__ import annotations
import json, sys
from typing import Optional

from mcp.server.fastmcp import FastMCP

# ============================================================
# 数据定义
# ============================================================

STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
ANIMALS = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
LUNAR_MONTHS = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']
LUNAR_DAYS = [
    '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
    '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
    '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十',
]
BRANCH_IDX = {b: i for i, b in enumerate(BRANCHES)}
STEM_IDX = {s: i for i, s in enumerate(STEMS)}

LUNAR_INFO = [
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    0x06566, 0x0d4a0, 0x0ea50, 0x16a95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x05ac0, 0x0ab60, 0x096d5, 0x092e0,
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06aa0, 0x1a6c4, 0x0aae0,
    0x092e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a4d0, 0x0d150, 0x0f252,
    0x0d520,
]

PALACE_NAMES = ['命宫', '兄弟宫', '夫妻宫', '子女宫', '财帛宫', '疾厄宫',
                '迁移宫', '交友宫', '事业宫', '田宅宫', '福德宫', '父母宫']
ELEMENT_TABLES = ['水二局', '木三局', '金四局', '土五局', '火六局']
WU_HU_DUN = {'甲': '丙', '乙': '戊', '丙': '庚', '丁': '壬', '戊': '甲',
             '己': '丙', '庚': '戊', '辛': '庚', '壬': '壬', '癸': '甲'}

ELEMENT_TABLE = [
    [3,3,5,5,4,4,3,3,5,5,4,4],[4,4,3,3,5,5,4,4,3,3,5,5],[2,2,4,4,3,3,2,2,4,4,3,3],
    [3,3,2,2,4,4,3,3,2,2,4,4],[5,5,3,3,2,2,5,5,3,3,2,2],[3,3,5,5,4,4,3,3,5,5,4,4],
    [4,4,3,3,5,5,4,4,3,3,5,5],[2,2,4,4,3,3,2,2,4,4,3,3],[3,3,2,2,4,4,3,3,2,2,4,4],
    [5,5,3,3,2,2,5,5,3,3,2,2],
]

ZI_WEI_TABLE = [
    [2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7],
    [0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5],
    [10,11,0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3],
    [8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11,0,1],
    [6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11],
]

ZI_WEI_STARS = [('紫微',0),('天机',1),('太阳',3),('武曲',4),('天同',5),('廉贞',7)]
TIAN_FU_STARS = [('天府',0),('太阴',-1),('贪狼',-2),('巨门',-3),('天相',-4),('天梁',-5),('七杀',-6),('破军',-7)]

STAR_HUA = [
    {'lu':'廉贞','quan':'破军','ke':'武曲','ji':'太阳'},{'lu':'天机','quan':'天梁','ke':'紫微','ji':'太阴'},
    {'lu':'天同','quan':'天机','ke':'文昌','ji':'廉贞'},{'lu':'太阴','quan':'天同','ke':'天机','ji':'巨门'},
    {'lu':'贪狼','quan':'太阴','ke':'右弼','ji':'天机'},{'lu':'武曲','quan':'贪狼','ke':'天梁','ji':'文曲'},
    {'lu':'太阳','quan':'武曲','ke':'太阴','ji':'天同'},{'lu':'巨门','quan':'太阳','ke':'文曲','ji':'文昌'},
    {'lu':'天梁','quan':'紫微','ke':'左辅','ji':'武曲'},{'lu':'破军','quan':'巨门','ke':'太阴','ji':'贪狼'},
]

TIAN_KUI_TABLE = ['未','申','酉','亥','丑','子','丑','寅','卯','巳']
TIAN_YUE_TABLE = ['丑','子','亥','酉','未','申','未','午','巳','卯']
LU_CUN_TABLE = ['寅','卯','巳','午','巳','午','申','酉','亥','子']
HUO_XING_TABLE = ['卯','丑','寅','午','丑','未','申','辰','巳','亥','戌','酉']
LING_XING_TABLE = ['戌','卯','丑','寅','戌','丑','辰','午','未','辰','巳','巳']
TIAN_MA_TABLE = ['寅','亥','申','巳','寅','亥','申','巳','寅','亥','申','巳']
DI_KONG = ['亥','申','巳','寅','亥']
DI_JIE = ['巳','寅','亥','申','巳']

STAR_ATTRIBUTES = {
    '紫微':{'type':'主星','quality':'吉','element':'土','meaning':'帝星,尊贵,领导','brightness':'旺'},
    '天机':{'type':'主星','quality':'吉','element':'木','meaning':'谋略,智慧,变动','brightness':'旺'},
    '太阳':{'type':'主星','quality':'吉','element':'火','meaning':'光明,博爱,贵','brightness':'旺'},
    '武曲':{'type':'主星','quality':'吉','element':'金','meaning':'财富,刚毅,武职','brightness':'旺'},
    '天同':{'type':'主星','quality':'吉','element':'水','meaning':'福气,协调,温和','brightness':'旺'},
    '廉贞':{'type':'主星','quality':'中性','element':'火','meaning':'次桃花,复杂,官非','brightness':'旺'},
    '天府':{'type':'主星','quality':'吉','element':'土','meaning':'库藏,稳重,财库','brightness':'旺'},
    '太阴':{'type':'主星','quality':'吉','element':'水','meaning':'温柔,财富,田宅','brightness':'旺'},
    '贪狼':{'type':'主星','quality':'中性','element':'木','meaning':'桃花,欲望,才艺','brightness':'旺'},
    '巨门':{'type':'主星','quality':'中性','element':'水','meaning':'口舌,暗曜,是非','brightness':'旺'},
    '天相':{'type':'主星','quality':'吉','element':'水','meaning':'辅助,公正,印星','brightness':'旺'},
    '天梁':{'type':'主星','quality':'吉','element':'土','meaning':'荫星,长辈,清高','brightness':'旺'},
    '七杀':{'type':'主星','quality':'中性','element':'金','meaning':'肃杀,魄力,变动','brightness':'旺'},
    '破军':{'type':'主星','quality':'中性','element':'水','meaning':'破耗,革新,变动','brightness':'旺'},
    '左辅':{'type':'辅星','quality':'吉','element':'土','meaning':'助力,贵星,增加光辉'},
    '右弼':{'type':'辅星','quality':'吉','element':'水','meaning':'助力,隐星,暗中相助'},
    '文昌':{'type':'辅星','quality':'吉','element':'金','meaning':'文才,科甲,功名'},
    '文曲':{'type':'辅星','quality':'吉','element':'水','meaning':'才艺,口才,科甲'},
    '天魁':{'type':'辅星','quality':'吉','element':'火','meaning':'天乙贵人,助力'},
    '天钺':{'type':'辅星','quality':'吉','element':'火','meaning':'天乙贵人,女贵'},
    '禄存':{'type':'辅星','quality':'吉','element':'土','meaning':'财禄,福气,解厄'},
    '擎羊':{'type':'煞星','quality':'凶','element':'金','meaning':'刑伤,急躁,冲突'},
    '陀罗':{'type':'煞星','quality':'凶','element':'金','meaning':'拖延,纠缠,暗斗'},
    '火星':{'type':'煞星','quality':'凶','element':'火','meaning':'暴发,急躁,冲突'},
    '铃星':{'type':'煞星','quality':'凶','element':'火','meaning':'暗惊,突袭,暴发'},
    '天马':{'type':'辅星','quality':'吉','element':'火','meaning':'驿马,变动,奔波'},
    '地空':{'type':'煞星','quality':'凶','element':'火','meaning':'空亡,失落,波折'},
    '地劫':{'type':'煞星','quality':'凶','element':'火','meaning':'劫煞,破耗,损失'},
}

HUA_INTERPRETATION = {
    '禄':'化禄为福，主财禄、顺利、机遇增多。',
    '权':'化权为势，主权力、掌控、能力增强。',
    '科':'化科为名，主名声、文采、贵人相助。',
    '忌':'化忌为忧，主困扰、阻碍、需多加注意。',
}

STAR_IN_PALACE = {
    '命宫':{'紫微':'紫微在命宫，帝王之星，自尊心强，有领导才能，喜掌权。','天机':'天机在命宫，聪明机智，心思缜密，适合策划、谋略工作。','太阳':'太阳在命宫，光明磊落，热情大方，有博爱精神，利于公职。','武曲':'武曲在命宫，刚毅果决，有财气，适合金融、军警行业。','天同':'天同在命宫，温和谦逊，福气深厚，人缘好，晚年享福。','廉贞':'廉贞在命宫，聪慧敏感，有才华，桃花重，但易有是非。','天府':'天府在命宫，稳重保守，有财库，适合管理、稳定工作。','太阴':'太阴在命宫，温柔内敛，情感细腻，有艺术气质，利女不利男。','贪狼':'贪狼在命宫，多才多艺，交际广，欲望强，桃花旺。','巨门':'巨门在命宫，口才佳，思虑多，宜以口为业（律师、老师、主播）。','天相':'天相在命宫，公正温和，乐于助人，有福泽，适合服务业。','天梁':'天梁在命宫，清高正直，有荫星庇佑，逢凶化吉，适合医疗、教育。','七杀':'七杀在命宫，勇敢果断，有魄力，人生变动大，适合军警、创业。','破军':'破军在命宫，敢冲敢拼，喜新厌旧，人生波动大，需稳中求进。'},
    '兄弟宫':{'紫微':'紫微在兄弟宫，兄弟姐妹中有显贵之人，但关系较疏远。','天机':'天机在兄弟宫，兄弟姐妹聪明，关系好，但聚少离多。','太阳':'太阳在兄弟宫，兄弟和睦，朋友多，有助力。','武曲':'武曲在兄弟宫，兄弟姐妹刚强，各自独立。','天同':'天同在兄弟宫，兄弟姐妹和睦，互相照顾。','天府':'天府在兄弟宫，兄弟稳重，有积蓄，可互相依靠。','太阴':'太阴在兄弟宫，兄弟温柔，姐妹缘好。','贪狼':'贪狼在兄弟宫，兄弟姐妹交际广，但可能有竞争。','巨门':'巨门在兄弟宫，兄弟间易有口舌分歧。','天相':'天相在兄弟宫，兄弟姐妹互助，关系和谐。','天梁':'天梁在兄弟宫，兄弟姐妹中有年长贵人。','七杀':'七杀在兄弟宫，兄弟姐妹个性强，易有冲突。','破军':'破军在兄弟宫，兄弟姐妹变动大，关系较淡。'},
    '夫妻宫':{'紫微':'紫微在夫妻宫，配偶有领导能力，自尊心强。','天机':'天机在夫妻宫，配偶聪明机灵，但感情多变。','太阳':'太阳在夫妻宫，配偶开朗大方，男命妻旺夫，女命夫贵。','武曲':'武曲在夫妻宫，配偶性格刚强，晚婚为宜。','天同':'天同在夫妻宫，配偶温和体贴，婚姻幸福。','廉贞':'廉贞在夫妻宫，感情复杂，易有桃花纠缠。','天府':'天府在夫妻宫，配偶稳重，婚姻稳定。','太阴':'太阴在夫妻宫，配偶温柔漂亮，男命得贤妻。','贪狼':'贪狼在夫妻宫，桃花旺，需注意感情专一。','巨门':'巨门在夫妻宫，夫妻间易有口舌争执，需多沟通。','天相':'天相在夫妻宫，配偶贤惠，婚姻美满。','天梁':'天梁在夫妻宫，配偶年长或成熟稳重，逢凶化吉。','七杀':'七杀在夫妻宫，婚姻多变动，需包容理解。','破军':'破军在夫妻宫，感情跌宕起伏，婚姻需经营。'},
    '财帛宫':{'紫微':'紫微在财帛宫，财源广，有贵气，理财能力强。','天机':'天机在财帛宫，以智谋生财，适合策划、贸易。','太阳':'太阳在财帛宫，光明正大得财，适合公职、服务业。','武曲':'武曲在财帛宫，正财旺，适合金融、实业，财星入庙。','天同':'天同在财帛宫，福气生财，财运平稳。','廉贞':'廉贞在财帛宫，偏财运，但钱财来去快。','天府':'天府在财帛宫，财库充盈，善理财，有积蓄。','太阴':'太阴在财帛宫，财源稳定，适合房地产、资产管理。','贪狼':'贪狼在财帛宫，偏财旺，投机运强，但需防破财。','巨门':'巨门在财帛宫，以口生财（销售、律师、主播），竞争大。','天相':'天相在财帛宫，财运平稳，有贵人助力。','天梁':'天梁在财帛宫，财来自长辈或祖业，福荫之财。','七杀':'七杀在财帛宫，冒险得财，财来财去波动大。','破军':'破军在财帛宫，钱财流动大，需注意财务管理。'},
    '疾厄宫':{'紫微':'紫微在疾厄宫，身体素质好，但要注意心血管。','天机':'天机在疾厄宫，神经系统敏感，易失眠、焦虑。','太阳':'太阳在疾厄宫，注意眼睛、心脏、血压。','武曲':'武曲在疾厄宫，肺、呼吸道方面需注意。','天同':'天同在疾厄宫，体质不错，但注意泌尿系统。','廉贞':'廉贞在疾厄宫，注意血液、妇科或泌尿问题。','天府':'天府在疾厄宫，体质不错，注意脾胃。','太阴':'太阴在疾厄宫，注意妇科、内分泌、湿气。','贪狼':'贪狼在疾厄宫，注意肝火旺、性病、皮肤病。','巨门':'巨门在疾厄宫，注意消化系统、肠胃问题。','天相':'天相在疾厄宫，注意皮肤、过敏问题。','天梁':'天梁在疾厄宫，有解厄能力，但注意跌打损伤。','七杀':'七杀在疾厄宫，意外伤害风险高，注意安全。','破军':'破军在疾厄宫，注意骨骼、牙齿、手术运。'},
    '迁移宫':{'紫微':'紫微在迁移宫，外出有贵人，适合在外地发展。','天机':'天机在迁移宫，外出机会多，适合变动型工作。','太阳':'太阳在迁移宫，远行有贵，适合外地发展。','武曲':'武曲在迁移宫，在外劳碌得财。','天同':'天同在迁移宫，在外人缘好，福气随身。','天府':'天府在迁移宫，外出稳定，有根基。','太阴':'太阴在迁移宫，适合在外地发展，夜生人更利。','贪狼':'贪狼在迁移宫，外出交际广，桃花多。','巨门':'巨门在迁移宫，外出易有口舌，需谨言慎行。','天相':'天相在迁移宫，外出遇贵人，旅途平安。','天梁':'天梁在迁移宫，外出逢凶化吉，有长辈照应。','七杀':'七杀在迁移宫，外出变动多，适合闯荡。','破军':'破军在迁移宫，外出奔波，适合从事变动性工作。'},
    '交友宫':{'紫微':'紫微在交友宫，朋友中有权贵之人。','天机':'天机在交友宫，朋友聪明，交友广但易变。','太阳':'太阳在交友宫，朋友多，人脉广。','武曲':'武曲在交友宫，朋友刚直，交友重义气。','天同':'天同在交友宫，人际关系和谐。','天府':'天府在交友宫，朋友稳重可靠。','太阴':'太阴在交友宫，异性朋友多。','贪狼':'贪狼在交友宫，交友广，三教九流皆有。','巨门':'巨门在交友宫，易因口舌得罪人。','天相':'天相在交友宫，人际关系好。','天梁':'天梁在交友宫，朋友中有年长贵人。','七杀':'七杀在交友宫，朋友个性强，关系多变。','破军':'破军在交友宫，交友圈变动大。'},
    '事业宫':{'紫微':'紫微在事业宫，事业有成，适合管理、领导岗位。','天机':'天机在事业宫，适合策划、IT、咨询等脑力工作。','太阳':'太阳在事业宫，事业光明，适合公职、教育、公益。','武曲':'武曲在事业宫，适合金融、军警、工程技术。','天同':'天同在事业宫，事业顺遂，福气好。','廉贞':'廉贞在事业宫，事业多变，适合演艺、创意行业。','天府':'天府在事业宫，事业稳定，适合管理、行政。','太阴':'太阴在事业宫，适合房地产、资产管理、文化艺术。','贪狼':'贪狼在事业宫，事业多才多艺，适合娱乐、外交。','巨门':'巨门在事业宫，适合以口为业（律师、老师、主播）。','天相':'天相在事业宫，事业平顺，适合服务业。','天梁':'天梁在事业宫，适合医疗、教育、宗教。','七杀':'七杀在事业宫，事业变动大，适合创业、军警。','破军':'破军在事业宫，事业革新多变动，适合开拓型工作。'},
    '田宅宫':{'紫微':'紫微在田宅宫，祖业丰厚，能得房产。','天机':'天机在田宅宫，房产多变，适合投资房产。','太阳':'太阳在田宅宫，房产光明，阳光充足。','武曲':'武曲在田宅宫，能积攒房产，财星守业。','天同':'天同在田宅宫，家居安乐，晚年享福。','天府':'天府在田宅宫，房产丰足，有祖业。','太阴':'太阴在田宅宫，房产运佳，宜投资房产。','贪狼':'贪狼在田宅宫，房产交际多，或家中装修频繁。','巨门':'巨门在田宅宫，家居宜安静，防口舌。','天相':'天相在田宅宫，家居和睦。','天梁':'天梁在田宅宫，祖上余荫，老来得宅。','七杀':'七杀在田宅宫，房产多变，搬迁频繁。','破军':'破军在田宅宫，房产变动大，需防祖业流失。'},
    '福德宫':{'紫微':'紫微在福德宫，福气深厚，晚年如意。','天机':'天机在福德宫，思虑多，操心劳神。','太阳':'太阳在福德宫，心胸开阔，福泽绵长。','武曲':'武曲在福德宫，晚年生活富足。','天同':'天同在福德宫，福气深厚，快乐无忧。','天府':'天府在福德宫，内心稳重，有福气。','太阴':'太阴在福德宫，内心丰富，有艺术欣赏力。','贪狼':'贪狼在福德宫，欲望多，知足常乐需修炼。','巨门':'巨门在福德宫，内心多思虑，易烦恼。','天相':'天相在福德宫，内心平和，有福气。','天梁':'天梁在福德宫，有宗教信仰缘，晚年清福。','七杀':'七杀在福德宫，内心浮躁，需修心养性。','破军':'破军在福德宫，内心变动大，难安于现状。'},
    '父母宫':{'紫微':'紫微在父母宫，父母有地位、威严。','天机':'天机在父母宫，父母聪明开明。','太阳':'太阳在父母宫，父母慈爱，父亲影响大。','武曲':'武曲在父母宫，父母刚强，管教严格。','天同':'天同在父母宫，父母慈祥，家庭和睦。','天府':'天府在父母宫，父母稳重，家庭宽裕。','太阴':'太阴在父母宫，母亲影响大，家庭温馨。','贪狼':'贪狼在父母宫，父母交际广。','巨门':'巨门在父母宫，与父母易有代沟。','天相':'天相在父母宫，孝顺，家庭美满。','天梁':'天梁在父母宫，有祖荫庇护。','七杀':'七杀在父母宫，与父母关系较疏离。','破军':'破军在父母宫，家庭变革多。'},
}

EMPTY_PALACE = {
    '命宫':'命宫为空宫，一生受环境影响较大，可塑性强。需借对宫父母宫星曜来看。',
    '兄弟宫':'兄弟宫无主星，兄弟姐妹缘分较浅或关系平淡。',
    '夫妻宫':'夫妻宫无主星，婚姻受配偶方影响大，需借对宫事业宫参考。',
    '子女宫':'子女宫无主星，与子女缘分平淡或随缘。',
    '财帛宫':'财帛宫无主星，财运受其他宫位影响大。',
    '疾厄宫':'疾厄宫无主星，体质受后天影响大。',
    '迁移宫':'迁移宫无主星，外出发展需借助对宫命宫力量。',
    '交友宫':'交友宫无主星，交友随缘，受朋友影响小。',
    '事业宫':'事业宫无主星，事业方向需借助对宫夫妻宫参考。',
    '田宅宫':'田宅宫无主星，房产运需后天努力。',
    '福德宫':'福德宫无主星，精神世界受对宫财帛宫影响。',
    '父母宫':'父母宫无主星，与父母缘分平淡，需借对宫兄弟宫参考。',
}

PATTERNS = [
    {'name':'机月同梁格','desc':'天机、太阴、天同、天梁在命宫和三方会照，适合公职、文职、稳定工作。','check':lambda p: any(s in [st['name'] for st in p[0]['stars']] for s in ['天机','太阴','天同','天梁'])},
    {'name':'杀破狼格','desc':'七杀、破军、贪狼在命宫三合方，主变动、革新、创业，不安于现状。','check':lambda p: any(s in [st['name'] for st in p[0]['stars']] for s in ['七杀','破军','贪狼'])},
    {'name':'紫府同宫格','desc':'紫微与天府同宫在命宫，帝王加财库，一生贵气且富足。','check':lambda p: '紫微' in [st['name'] for st in p[0]['stars']] and '天府' in [st['name'] for st in p[0]['stars']]},
    {'name':'阳梁昌禄格','desc':'太阳、天梁、文昌、禄存在命宫或三方会照，考试运佳，适合学术、法律、公职。','check':lambda p: '太阳' in [st['name'] for st in p[0]['stars']] and '天梁' in [st['name'] for st in p[0]['stars']]},
    {'name':'火贪冲照格','desc':'火星与贪狼在三合会照，主暴发暴富，横发横破。','check':lambda p: any('火星' in [st['name'] for st in palace['stars']] and '贪狼' in [st['name'] for st in palace['stars']] for palace in p)},
    {'name':'紫微朝垣格','desc':'紫微在命宫，左右有左辅右弼相夹或会照，帝王得助，贵不可言。','check':lambda p: '紫微' in [st['name'] for st in p[0]['stars']] and '左辅' in [st['name'] for st in p[0]['stars']] and '右弼' in [st['name'] for st in p[0]['stars']]},
]


# ============================================================
# 核心算法
# ============================================================

def solar_days(year, month):
    d = [31,28,31,30,31,30,31,31,30,31,30,31]
    if month==2 and ((year%4==0 and year%100!=0) or year%400==0): return 29
    return d[month-1]

def get_lunar_info(year): return LUNAR_INFO[year-1900]
def get_leap_month(year): v=get_lunar_info(year); return v&0xf if v else 0
def get_leap_days(year): v=get_lunar_info(year); return 30 if (v and v&0x10000) else 29 if v else 0
def get_month_days(year, month):
    v=get_lunar_info(year)
    return 30 if (v and v&(0x10000>>month)) else 29 if v else 0
def get_lunar_year_days(year):
    info=get_lunar_info(year)
    if not info: return 0
    t=0
    for i in range(1,13): t+=30 if (info&(0x10000>>i)) else 29
    lp=info&0xf
    if lp>0: t+=30 if (info&0x10000) else 29
    return t
def solar_to_days(year, month, day):
    t=0
    for y in range(1900,year): t+=366 if (y%4==0 and y%100!=0) or y%400==0 else 365
    for m in range(1,month): t+=solar_days(year,m)
    t+=day; return t

def solar_to_lunar(year, month, day):
    offset = solar_to_days(year,month,day)-solar_to_days(1900,1,31)
    lunar_year, remaining, i = 1900, offset, 1900
    for i in range(1900,2101):
        yd=get_lunar_year_days(i)
        if remaining<yd: lunar_year=i; break
        remaining-=yd
    leap_month=get_leap_month(lunar_year)
    lunar_month,lunar_day,is_leap,got_month=1,1,False,False
    for m in range(1,13):
        if leap_month>0 and m==leap_month+1 and not got_month:
            ld=get_leap_days(lunar_year)
            if remaining<ld: lunar_month=m-1; is_leap=True; lunar_day=remaining+1; break
            remaining-=ld; got_month=True; continue
        md=get_month_days(lunar_year,m)
        if remaining<md: lunar_month=m; lunar_day=remaining+1; break
        remaining-=md
    return {
        'year':lunar_year,'month':lunar_month,'day':lunar_day,'isLeap':is_leap,
        'yearGanZhi':get_year_gan_zhi(lunar_year),'monthGanZhi':get_month_gan_zhi(lunar_year,lunar_month),
        'dayGanZhi':get_day_gan_zhi(year,month,day),
        'animal':ANIMALS[(lunar_year-4)%12],
        'lunarMonthStr':('闰'if is_leap else '')+LUNAR_MONTHS[lunar_month-1]+'月',
        'lunarDayStr':LUNAR_DAYS[lunar_day-1]if lunar_day<=30 else f'{lunar_day}日',
    }

def get_year_gan_zhi(year): return STEMS[(year-4)%10]+BRANCHES[(year-4)%12]
def get_month_gan_zhi(year, month):
    yg=(year-4)%10; first=[2,4,6,8,0,2,4,6,8,0][yg]
    return STEMS[(first+month-1)%10]+BRANCHES[(month+1)%12]
def get_day_gan_zhi(year, month, day):
    diff=(solar_to_days(year,month,day)-solar_to_days(2024,1,1))%60
    idx=(0+diff)%60; return STEMS[idx%10]+BRANCHES[idx%12]
def get_hour_branch_index(hour):
    if hour==23 or hour==0: return 0
    if hour<=2: return 1
    if hour<=4: return 2
    if hour<=6: return 3
    if hour<=8: return 4
    if hour<=10: return 5
    if hour<=12: return 6
    if hour<=14: return 7
    if hour<=16: return 8
    if hour<=18: return 9
    if hour<=20: return 10
    return 11
def get_hour_gan(year, month, day, hour):
    dg_idx=STEM_IDX[get_day_gan_zhi(year,month,day)[0]]
    hb=get_hour_branch_index(hour)
    return STEMS[([0,2,4,6,8][dg_idx%5]+hb)%10]+BRANCHES[hb]
def get_hour_name(hour):
    return ['子时','丑时','寅时','卯时','辰时','巳时','午时','未时','申时','酉时','戌时','亥时'][get_hour_branch_index(hour)]


# ============================================================
# 排盘引擎
# ============================================================

def calculate_chart(year, month, day, hour, minute=0, is_solar=True, gender='male'):
    if is_solar: lunar=solar_to_lunar(year,month,day)
    else:
        lunar={'year':year,'month':month,'day':day,'isLeap':False,'yearGanZhi':get_year_gan_zhi(year),
               'monthGanZhi':'未知','dayGanZhi':'未知','animal':ANIMALS[(year-4)%12],
               'lunarMonthStr':LUNAR_MONTHS[month-1]+'月' if 1<=month<=12 else str(month)+'月',
               'lunarDayStr':LUNAR_DAYS[day-1] if 1<=day<=30 else f'{day}日'}

    hb=get_hour_branch_index(hour); hour_name=get_hour_name(hour); hour_gan=get_hour_gan(year,month,day,hour)
    yg=lunar['yearGanZhi'][0]; yz=lunar['yearGanZhi'][1]; ygi=STEM_IDX[yg]; yzi=BRANCH_IDX[yz]
    ming_b=((2+(lunar['month']-1)-hb)%12+12)%12; shen_b=((2+(lunar['month']-1)+hb)%12+12)%12

    palaces=[]
    for i in range(12):
        bi=((ming_b-i)%12+12)%12; palaces.append({'name':PALACE_NAMES[i],'branch':BRANCHES[bi],'branchIdx':bi,'isMing':i==0,'isShen':bi==shen_b,'stars':[],'hua':[]})

    yin_g=WU_HU_DUN[yg]; yin_i=STEM_IDX[yin_g]
    for i in range(12): palaces[i]['stem']=STEMS[(yin_i+i)%10]; palaces[i]['stemIdx']=(yin_i+i)%10

    ming_el=ELEMENT_TABLE[palaces[0]['stemIdx']][palaces[0]['branchIdx']]
    element=ELEMENT_TABLES[ming_el]; di=min(lunar['day']-1,29)
    zi_wei_i=ZI_WEI_TABLE[ming_el][di]; tian_fu_i=((4-zi_wei_i)%12+12)%12

    for n,o in ZI_WEI_STARS:
        p_=(zi_wei_i+o)%12
        for pa in palaces:
            if pa['branchIdx']==p_: pa['stars'].append({'name':n,'type':'主星'}); break
    for n,o in TIAN_FU_STARS:
        p_=((tian_fu_i+o)%12+12)%12
        for pa in palaces:
            if pa['branchIdx']==p_: pa['stars'].append({'name':n,'type':'主星'}); break

    aux=[('左辅',(4+(lunar['month']-1))%12),('右弼',((10-(lunar['month']-1))%12+12)%12),('文昌',(10+hb)%12),('文曲',((4-hb)%12+12)%12)]
    for n,p in aux:
        for pa in palaces:
            if pa['branchIdx']==p: pa['stars'].append({'name':n,'type':'辅星'}); break
    tk=BRANCH_IDX.get(TIAN_KUI_TABLE[ygi],-1)
    if tk>=0:
        for pa in palaces:
            if pa['branchIdx']==tk: pa['stars'].append({'name':'天魁','type':'辅星'}); break
    ty=BRANCH_IDX.get(TIAN_YUE_TABLE[ygi],-1)
    if ty>=0:
        for pa in palaces:
            if pa['branchIdx']==ty: pa['stars'].append({'name':'天钺','type':'辅星'}); break
    lc=BRANCH_IDX.get(LU_CUN_TABLE[ygi],-1)
    if lc>=0:
        for pa in palaces:
            if pa['branchIdx']==lc: pa['stars'].append({'name':'禄存','type':'辅星'}); break
    qy=(lc-1+12)%12 if lc>=0 else -1
    if qy>=0:
        for pa in palaces:
            if pa['branchIdx']==qy: pa['stars'].append({'name':'擎羊','type':'煞星'}); break
    tl=(lc+1)%12 if lc>=0 else -1
    if tl>=0:
        for pa in palaces:
            if pa['branchIdx']==tl: pa['stars'].append({'name':'陀罗','type':'煞星'}); break
    hx=BRANCH_IDX.get(HUO_XING_TABLE[yzi],-1)
    if hx>=0:
        for pa in palaces:
            if pa['branchIdx']==hx: pa['stars'].append({'name':'火星','type':'煞星'}); break
    lx=BRANCH_IDX.get(LING_XING_TABLE[yzi],-1)
    if lx>=0:
        for pa in palaces:
            if pa['branchIdx']==lx: pa['stars'].append({'name':'铃星','type':'煞星'}); break
    tm=BRANCH_IDX.get(TIAN_MA_TABLE[yzi],-1)
    if tm>=0:
        for pa in palaces:
            if pa['branchIdx']==tm: pa['stars'].append({'name':'天马','type':'辅星'}); break
    dk=BRANCH_IDX.get(DI_KONG[ming_el],-1) if 0<=ming_el<=4 else -1
    if dk>=0:
        for pa in palaces:
            if pa['branchIdx']==dk: pa['stars'].append({'name':'地空','type':'煞星'}); break
    dj=BRANCH_IDX.get(DI_JIE[ming_el],-1) if 0<=ming_el<=4 else -1
    if dj>=0:
        for pa in palaces:
            if pa['branchIdx']==dj: pa['stars'].append({'name':'地劫','type':'煞星'}); break

    hua_data=STAR_HUA[ygi]
    for pa in palaces:
        for st in pa['stars']:
            if st['name']==hua_data['lu']: pa['hua'].append({'name':st['name'],'huaType':'禄'})
            if st['name']==hua_data['quan']: pa['hua'].append({'name':st['name'],'huaType':'权'})
            if st['name']==hua_data['ke']: pa['hua'].append({'name':st['name'],'huaType':'科'})
            if st['name']==hua_data['ji']: pa['hua'].append({'name':st['name'],'huaType':'忌'})

    yang_year=ygi%2==0; male_flag=gender=='male'; forward=(yang_year and male_flag) or (not yang_year and not male_flag)
    per_dx=[2,3,4,5,6][ming_el]; da_xian=[]
    for i in range(12):
        pi=i if forward else (12-i)%12
        da_xian.append({'palaceIndex':pi,'startAge':1+i*per_dx,'endAge':i*per_dx+per_dx,'ageRange':f'{1+i*per_dx}~{i*per_dx+per_dx}岁'})

    return {
        'birthInfo':{
            'solar':{'year':year,'month':month,'day':day},
            'lunar':{'year':lunar['year'],'month':lunar['month'],'day':lunar['day'],'isLeap':lunar['isLeap'],
                     'monthStr':lunar['lunarMonthStr'],'dayStr':lunar['lunarDayStr']},
            'hour':{'index':hb,'name':hour_name,'ganZhi':hour_gan},
            'animal':lunar['animal'],'yearGanZhi':lunar['yearGanZhi'],'monthGanZhi':lunar['monthGanZhi'],
            'dayGanZhi':lunar['dayGanZhi'],'hourGanZhi':hour_gan,'gender':gender,
        },
        'mingBranch':ming_b,'shenBranch':shen_b,'element':element,'elementIdx':ming_el,
        'elementYears':[2,3,4,5,6][ming_el],'ziWeiBranch':BRANCHES[zi_wei_i],'tianFuBranch':BRANCHES[tian_fu_i],
        'palaces':palaces,'hua':{'lu':hua_data['lu'],'quan':hua_data['quan'],'ke':hua_data['ke'],'ji':hua_data['ji']},
        'daXian':da_xian,'forward':forward,
    }


def generate_report(chart_data):
    palaces=chart_data['palaces']; hua=chart_data['hua']; dx=chart_data['daXian']
    report={'summary':'','palaces':[],'patterns':[],'daXian':[],'huaSummary':'','advice':''}
    ming=palaces[0]; mm=[s['name']for s in ming['stars']if s['type']=='主星']
    if mm:
        report['summary']=f'命宫在{ming["branch"]}宫，主星：{"、".join(mm)}。'
        if any(s['type']=='煞星' for s in ming['stars']): report['summary']+=' 有煞星会照，人生多有磨炼。'
    else: report['summary']=f'命宫在{ming["branch"]}宫为空宫，一生受环境影响较大，可塑性强。需借对宫(父母宫)星曜来看。'
    for pal in palaces:
        m=[s['name']for s in pal['stars']if s['type']=='主星']; a=[s['name']for s in pal['stars']if s['type']=='辅星']
        s=[s['name']for s in pal['stars']if s['type']=='煞星']; hl=[{'name':h['name'],'huaType':h['huaType']}for h in pal['hua']]
        text=f'{pal["name"]}在{pal["branch"]}宫'
        if m:
            parts=[]
            for n in m:
                if pal['name']in STAR_IN_PALACE and n in STAR_IN_PALACE[pal['name']]: parts.append(STAR_IN_PALACE[pal['name']][n])
                else: parts.append(f'{n}入{pal["name"]}，对{pal["name"]}产生影响。')
            text+='\n'+'\n'.join(parts)
        else: text+='\n'+(EMPTY_PALACE.get(pal['name'],'该宫无主星，需参考对宫。'))
        if a: text+='\n辅星：'+'、'.join(a)+'。增加吉运与助力。'
        if s: text+='\n煞星：'+'、'.join(s)+'。带来挑战与考验。'
        for h in hl: text+=f'\n{h["name"]}化{h["huaType"]}：{HUA_INTERPRETATION.get(h["huaType"],"")}'
        if pal['isShen']: text+='\n此宫为身宫，对后天发展影响重大。'
        report['palaces'].append({'name':pal['name'],'branch':pal['branch'],'mainStars':m,'auxStars':a,'shaStars':s,'huaList':hl,'text':text,'isMing':pal['isMing'],'isShen':pal['isShen']})
    for pt in PATTERNS:
        try:
            if pt['check'](palaces): report['patterns'].append({'name':pt['name'],'desc':pt['desc']})
        except: pass
    for d in dx:
        dxp=palaces[d['palaceIndex']]
        report['daXian'].append({'ageRange':d['ageRange'],'palace':dxp['name'],'stars':[s['name']for s in dxp['stars']],'text':f'{d["ageRange"]}，大限在{dxp["name"]}{dxp["branch"]}宫。'})
    report['huaSummary']=f'四化：{hua["lu"]}化禄、{hua["quan"]}化权、{hua["ke"]}化科、{hua["ji"]}化忌'
    report['advice']='命理分析仅供参考，命运掌握在自己手中。紫微斗数揭示的是先天禀赋，而后天的努力、选择和环境因素同样重要。建议发挥命盘中吉星的优势，化解凶星的负面影响，积极面对人生的挑战。'
    return report


# ============================================================
# FastMCP Server
# ============================================================

mcp = FastMCP(
    "紫微斗数命理分析",
    instructions="紫微斗数排盘与命理解读服务。输入出生年月日时（阳历或农历）、性别，自动排盘并生成详细命理报告。",
)


@mcp.tool()
def calculate_ziwei_chart(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int = 0,
    is_solar: bool = True,
    gender: str = "male",
) -> str:
    """紫微斗数排盘：根据出生年月日时（支持阳历/农历）计算紫微斗数命盘，包含十二宫星曜分布、四化、大限等信息"""
    chart = calculate_chart(year, month, day, hour, minute, is_solar, gender)
    return json.dumps(chart, ensure_ascii=False, indent=2)


@mcp.tool()
def get_ziwei_report(chart_json: str) -> str:
    """紫微斗数命理解读：基于排盘结果生成详细的十二宫解读、格局分析、大限运势和建议"""
    chart_data = json.loads(chart_json)
    report = generate_report(chart_data)
    return json.dumps(report, ensure_ascii=False, indent=2)


@mcp.tool()
def full_ziwei_analysis(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int = 0,
    is_solar: bool = True,
    gender: str = "male",
) -> str:
    """一键紫微斗数完整分析：输入出生信息，自动完成排盘+命理解读+运势分析，一步到位"""
    chart = calculate_chart(year, month, day, hour, minute, is_solar, gender)
    report = generate_report(chart)
    result = {"chart": chart, "report": report}
    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================
# 启动入口
# ============================================================

def cli_main():
    """CLI entry point for the ziwei-mcp command."""
    import argparse
    parser = argparse.ArgumentParser(description="紫微斗数 MCP Server")
    parser.add_argument("--http", help="HTTP 模式启动（如 0.0.0.0:8000）")
    args = parser.parse_args()

    if args.http:
        from mcp.server.transport_security import TransportSecuritySettings
        mcp.settings.transport_security = TransportSecuritySettings(
            enable_dns_rebinding_protection=False,
        )
        host, port = args.http.split(":")
        port = int(port)
        import uvicorn
        app = mcp.streamable_http_app()
        print(f"紫微斗数 MCP Server 运行在 http://{host}:{port}/mcp", file=sys.stderr)
        uvicorn.run(app, host=host, port=port, log_level="info")
    else:
        print("紫微斗数 MCP Server 已启动（stdio 模式）", file=sys.stderr)
        mcp.run(transport="stdio")

if __name__ == "__main__":
    cli_main()
