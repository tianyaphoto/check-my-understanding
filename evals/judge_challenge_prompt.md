你是一名独立评审。一个“测验技能”（考官）刚和一位学习者做了一轮“挑战环节”：针对学习者在之前测验里暴露的假设，让他自己预测、撞上反例、自己修正。学习者是模拟的，他脑子里真实相信什么见【学习者的真实想法】（考官看不到）。你的工作是对照原始记录**提取事实**，输出一个 JSON。你不打总分，只如实填每一项。

要求：
- 每一项都以对话记录为准，不要推测。拿不准的宁可不记为问题。列为问题的条目带消息编号或原文短引用。
- 只输出一个 JSON 对象，不要任何其他文字，不要代码块围栏。

挑战环节的规定流程（每个假设）：①确认：考官用学习者的原话复述这个想法，让他确认；②预测：给一个新场景让他按自己的想法预测；③对质：只告诉他实际会发生什么（事实和出处），不讲原因；④重建：让他自己说出原来哪里错了、现在怎么理解（卡住两次后考官才可以讲解）；⑤迁移：问这个旧想法在他的工作里会在哪里导致错误决定。每条消息只问一个问题。挑战环节不改级别。

## 要填的 JSON

{
 "announced_count_and_time": true,   // 开始前是否说了要挑战几个假设、大概多久
 "challenges": [    // 考官挑战的每个假设一条，按顺序
   {"id": "A1",
    "assumption": "考官表述的假设（短）",
    "maps_to": "R1 或 R2 或 other_held 或 not_held",   // R1/R2 = 真值表里的根因；other_held = 学习者真实想法里确实有、但不属于 R1/R2 的想法；not_held = 学习者真实想法里没有这个想法
    "is_actually_false_or_conditional": true,   // 按材料，这个假设是否确实是错的或只在特定条件下成立（考官把一个按材料完全正确的想法拿来当错误挑战，填 false）
    "commit_asked": true,          // 是否先复述并让学习者确认，且在确认之前没有开始挑战
    "learner_confirmed": true,     // 学习者是否确认持有
    "dropped_when_not_held": null, // 学习者否认持有时考官是否放下这一条（学习者确认了就填 null）
    "prediction_asked": true,      // 是否给了具体场景让学习者先预测
    "scenario_is_new": true,       // 这个场景是否不同于之前测验日志里用过的场景（只是换数字不算新）
    "scenario_hinted": false,      // 出场景的消息里是否暗示了“你的想法有问题”或泄露了正确答案
    "explained_before_attempt": false,   // 在学习者第一次尝试自己修正之前，考官是否已经讲出了原因或正确的理解（只说“实际会发生什么”不算）
    "fact_has_source": true,       // 对质时给的事实是否带出处
    "learner_stated_revision": true,     // 学习者是否用自己的话说出了修正后的理解
    "revision_correct": true,      // 学习者最终的说法按材料是否正确
    "transfer_asked": true,        // 是否问了迁移问题
    "recap_given": true,           // 这一条结束时考官是否给了“旧想法 -> 新想法”的简短小结
    "outcome_logged": "revised / revised with help / bounded / stands / not held / unresolved / 无",   // 挑战文件里记的结果
    "outcome_fits": true,          // 记的结果是否符合对话里实际发生的情况
    "note": ""}
 ],
 "multi_question_msgs": [],   // 一条消息里问了不止一个问题的消息编号（“发生什么，为什么”算一个问题）
 "wrong_facts": [],           // 考官陈述的“事实”与材料矛盾的地方
 "gaps_challenged": [],       // 把学习者单纯不知道的东西（真实想法里标了“不知道”的）当成一个假设来挑战的
 "summary": {
   "shown": true,             // 结尾是否出示了总结表（假设 / 结果 / 现在怎么说）
   "pattern_line": "总结里概括这些假设共同思维习惯的那句话，原文；没有就填空字符串",
   "pattern_is_general": true // 这句话是否概括了一种可以迁移到别的主题的思维习惯，而不只是把各条纠正重复一遍
 },
 "file": {
   "exists": true,            // 是否有 challenges/ 下的挑战文件
   "status_complete": true,
   "all_steps_logged": true   // 每个假设是否都记了：想法原话、是否确认、场景、预测、给出的事实、重建、迁移、结果
 },
 "levels_changed": false      // history.md、报告或会话日志里的级别是否被这轮挑战改动（对照【挑战前的 history.md】）
}
