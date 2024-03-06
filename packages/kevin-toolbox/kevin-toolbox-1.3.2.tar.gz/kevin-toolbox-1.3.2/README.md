# kevin_toolbox

一个通用的工具代码包集合



环境要求

```shell
numpy>=1.19
pytorch>=1.2
```

安装方法：

```shell
pip install kevin-toolbox  --no-dependencies
```



[项目地址 Repo](https://github.com/cantbeblank96/kevin_toolbox)

[使用指南 User_Guide](./notes/User_Guide.md)

[免责声明 Disclaimer](./notes/Disclaimer.md)

[版本更新记录](./notes/Release_Record.md)：

- v 1.3.2 （2024-03-05）【bug fix】【new feature】
  - patches
    - for_optuna.serialize
      - 【bug fix】fix bug in for_study.dump()，使用 try except 来捕抓并跳过使用 getattr(study, k) 读取 study 中属性时产生的错误。（比如单变量优化时的best_trials参数） 
      - 【bug fix】fix bug in for_study.dump()，避免意外修改 study 中的属性。
        - 添加了对应的测试用例。
    - for_matplotlib
      - 【new feature】add generate_color_list()，用于生成指定数量的颜色列表，支持对指定颜色的排除。
    - for_numpy
      - 【new feature】add linalg.entropy()，用于计算分布的熵。
      - 【new feature】add random，添加了用于随机生成的模块，其中包含：
        - get_rng()，获取默认随机生成器or根据指定的seed构建随机生成器。
        - truncated_normal()，从截断的高斯分布中进行随机采样。
        - truncated_multivariate_normal()，从截断的多维高斯分布中进行随机采样。
        - 添加了测试用例。
  - nested_dict_list
    - 【bug fix】fix bug in get_nodes()，修复了遍历非叶节点时，当节点下的叶节点均不存在时会异常跳过该节点的问题。
      - 添加了对应的测试用例。
    - 【new feature】modify set_default()，修改后将默认返回对应name的值，而不是返回整体的var，从而与python dict的setdefault函数的行为对齐。特别地，也支持通过设置b_return_var参数来获取 var。
      - 修改了对应的测试用例。
  - computer_science.algorithm
    - registration.Registry
      - 【new feature】改进 self.collect_from_paths() 函数。
        - 增加一个检查用于避免待搜索路径包含调用该函数的文件。如果包含，则报错，同时提示这样会导致  collect_from_paths() 函数被无限递归调用，从而引起死循环。并建议将该函数的调用位置放置在待搜索路径外，或者使用 ignore_s 将其进行屏蔽。 
        - 添加了测试用例。
      - 【bug fix】fix bug in self.get()，之前 get() 函数中只从 `self._item_to_add`和 `self._path_to_collect` 中加载一次注册成员，但是加载的过程中，可能后面因为对 `self._path_to_collect` 的加载，又往 `self._item_to_add` 中添加了待处理内容，导致不能完全加载。该问题已修复。
        - 添加了测试用例。
    - 【new feature】add cache_manager，新增了 cache_manager 模块用于进行缓存管理。
      - 其中主要包含三个部分：
        - 缓存数据结构：cache_manager.cache 和 `cache_manager.variable.CACHE_BUILDER_REGISTRY`
          - 基类：`Cache_Base`
          - 基于内存的缓存结构：`Memo_Cache`，注册名 `":in_memory:Memo_Cache"` 等等。
        - 缓存更新策略：cache_manager.strategy 和 `cache_manager.variable.CACHE_STRATEGY_REGISTRY`
          - 基类：`Strategy_Base`
          - 删除最后一次访问时间最久远的部分：`FIFO_Strategy`，注册名 `":by_initial_time:FIFO_Strategy"` 等等。
          - 删除访问频率最低的部分：`LFU_Strategy`，注册名 `":by_counts:LFU_Strategy"` 等等。
          - 删除最后一次访问时间最久远的部分：`LRU_Strategy`，注册名 `":by_last_time:LRU_Strategy"` 等等。
          - 删除访问频率最低的部分：`LST_Strategy`，注册名 `":by_survival_time:LST_Strategy"` 等等。
        - 缓存管理器：Cache_Manager（主要用这个）
      - 添加了测试用例。
  - data_flow.core.cache
    - modify Cache_Manager_for_Iterator，使用新增的 cache_manager 模块替换 Cache_Manager_for_Iterator 中基于内存的缓存。相关参数有修改。
      - 添加了测试用例。

