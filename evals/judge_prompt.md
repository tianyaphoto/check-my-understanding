你是一名独立评审。有一个“测验技能”（考官）刚给一位学习者做了一次理解程度测验。学习者是模拟的，他的真实水平是事先设定好的（见【真值表】），考官不知道。你的工作是对照真值表和原始记录，**提取事实**，输出一个 JSON。你不打总分，只如实填每一项。

要求：
- 每一项都以原始记录为准，不要推测。拿不准的宁可不记为问题。凡是列为问题的条目都要带题号或原文短引用，方便人工核实。
- 只输出一个 JSON 对象，不要任何其他文字，不要代码块围栏。

本次测验：学习者画像 = {profile}；类型 = {kind}（baseline 摸底 / retest 复测）。

## 要填的 JSON

{
 "nodes": [   // 考官知识树里的每个节点一条
   {"node": "N1", "name": "…", "weight": "core 或 supporting", "sections": ["S1"],   // 这个节点对应材料的哪几节
    "measured": 3,            // 考官本次最终报告给这个节点的级别，整数；报告写“未测”就填 "untested"
    "truth": 3,               // 按真值表本画像这一栏：节点只对应一节就取那一节的值；对应多节取平均后四舍五入
    "note": ""}
 ],
 "roots": [   // 真值表里本画像**当前仍然有**的每个根因（R1、R2）一条；本画像没有根因就给空数组
   {"id": "R1", "found": "root 或 mentioned 或 missed",   // root=报告的诊断里把它作为一条根本问题明确点出了这个错误模型；mentioned=只在别处顺带提到；missed=没有
    "quote": "报告里的原话（短）"}
 ],
 "false_roots": [ "报告诊断里断言学习者有某个错误心智模型，但按真值表他并没有（纯缺失被说成‘缺失’不算错；把不存在的错误观念安到他头上才算）。每条写报告原话" ],
 "gap_summary_ok": true,   // 报告对学习者整体状况的概括是否符合真值表“埋下的根因”一节对本画像的描述（例如 p3a 应被概括为只知道是什么、不知道为什么，而不是别的）
 "process": {
   "question_msgs": 0,          // 考官发出的、含有测验题的消息条数（不含开场确认、不含最终报告）
   "multi_question_msgs": [],   // 一条消息里出了不止一道新题的，列消息编号
   "feedback_expected": 0,      // 学习者作答后、考官本应先给讲评的次数（“追问为什么”之前只给对错不讲解是允许的，那一次算已给）
   "feedback_missing": [],      // 该给讲评却没有给出“对错判定 + 正确答案”的，列消息编号
   "feedback_without_source": 0,// 讲评里没有指出处（材料哪一节）的次数
   "mcq_total": 0,
   "mcq_without_idk": [],       // 没有“不知道”选项的选择题题号
   "hints_before_answer": [],   // 在学习者作答前就泄露答案或给提示的题号
   "no_progress_marker": 0,     // 出题消息里没有 Q7/20 这类进度标记的条数
   "questions_asked": 0,        // 计入预算的题数（含追问）
   "budget": 0,                 // 开场约定的题量
   "short_answer_total": 0
 },
 "integrity": {
   "wrong_keys": [],            // 考官认定的“正确答案”或讲评内容与材料矛盾，或选择题有两个都说得通的选项。格式 {"q":"Q5","why":"…"}
   "leaks_counted": [],         // 某题的答案已被本场更早的讲评直接说出过，学习者答对后考官仍据此抬高了级别。格式 {"q":"Q11","leaked_by":"Q1 讲评","why":"…"}
   "mislabeled_levels": [],     // 题目标注的目标级别与它实际考的认知层次差了至少 2 级（按通用量表：2 是什么/3 为什么/4 新场景与边界/5 取舍）。格式 {"q":"Q9","labeled":4,"actual":2}
   "log_fields_missing": [],    // 逐题日志应有：题目、目标节点和级别、学习者原话、判定、暴露的误解（如有）、本次讲评透露了什么、该节点当前级别估计。列出整体缺失的字段名
   "mastery_reported": 0,       // 报告里的掌握度百分数
   "mastery_recomputed": 0,     // 你按 sum(权重×min(级别,目标)) / sum(权重×目标) ×100 用报告里的各节点级别重算（core 权重 2，supporting 权重 1；未测节点按报告自己声明的处理方式算，报告没声明就按 0 算）
   "untested_rule_stated": true,// 没有未测节点填 true；有未测节点时，报告是否说明了它们怎么计入掌握度
   "history_row_written": true,
   "report_saved": true
 },
 "retest": null   // 摸底填 null；复测填下面的对象
 /* 复测时：
 {
   "changes": [ {"node":"N1","before":2,"after":4,"truth_before":3,"truth_after":4,
                 "reported_direction":"up/same/down","truth_direction":"up/same/down"} ],   // truth_before 取真值表里摸底画像那一栏
   "roots_status": [ {"id":"R1","reported":"resolved/partly/persists/not_mentioned","quote":"…"} ],   // 对真值表里摸底时存在的每个根因；若摸底报告没提出过这个根因而复测报告也没提，填 not_mentioned
   "mastered_declared": false,      // 报告是否明确宣布“已掌握”
   "core_nodes_at_target": 0, "core_nodes_total": 0,   // 按考官本次报告的级别
   "reused_questions": [],          // 与上一场日志里实质相同的题
   "rubric_edited": false           // tree.md 的节点、级别描述是否被改动（对照 changelog 与内容）
 } */
}

---
