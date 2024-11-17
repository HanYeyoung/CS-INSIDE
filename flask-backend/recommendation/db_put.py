import pandas as pd

# 데이터 전체
data = {
    "uuid": [
        "3795cfcc-807e-3ca7-8348-d4a909a42f06", "7ea3c96f-5246-39ac-9c22-eff420630de2",
        "60bf2c49-51e0-3f19-b9a5-04c55dbd3a7c", "cac576c6-784e-3f56-8a53-6000c77c9a70",
        "07eabcce-fdab-3781-99ca-7dc2dc3544ae", "613fbdc2-d4e9-3ac0-ae9b-af126ae97119",
        "28a2d3c7-60de-3cf1-80ff-e989f4d88350", "723bb90e-7865-35bf-b4f4-7f2978dbd413",
        "b2107f35-bc8a-3ce0-b17e-4270f762d07b", "73e639b4-409e-3bcd-9211-51eafa19a1b1",
        "cb48129f-99e6-36fa-9a20-46e0617e2499", "892c1608-d603-3e23-80b9-5db404724b39",
        "e449f054-a344-3556-b18a-5333e51ceb82", "14d37fdc-b58d-30df-af83-a32e1779c8d6",
        "c383953c-7c14-3614-b84e-107441ba5002", "4d059bd9-4520-3a4d-9174-e3ad726d085e",
        "88e440eb-1e19-3b5f-b7a7-bf29b505e9c3", "4c05436f-19b3-3f06-b99a-c28d268997f5",
        "d22643fc-796e-39f7-b078-2d62de0cf51d", "ecff4693-50ce-3960-91fe-374a8db40534",
        "e9a360bc-be2d-35d1-9684-a464bbbd0c15", "de8a0a8c-e076-3ec2-8b6c-e1e1ee82a53e",
        "d5fe8d3d-c558-3d58-a82f-7956ed122240", "323b9c99-a1d7-37d7-a524-7ad3d318b85d",
        "0792eac4-46ac-3e08-8cd0-858349ff66d1", "af9d93a2-e492-320d-af8d-9037cdbac6e5",
        "1f36cc02-0eee-3fcf-be09-1ad17aecf83c", "90d9a30d-6330-33f8-9aee-fe82055a4653",
        "f87b3a9c-34da-3fbf-8621-2a513cb3e4d1", "e6d6df0e-1456-36bb-81bc-5648cf0f224d"
    ],
    "name": [
        "Programming I", "Data Sci Programming I", "Introduction to Discrete Mathematics",
        "Introduction to Computer Engineering", "Programming II", "Introduction to Data Programming",
        "Introduction to Programming", "Problem Solving Using Computers", "Data Sci Programming II",
        "Digital System Fundamentals", "Machine Organization and Programming", 
        "Introduction to Data Structures", "Programming III", "Introduction to Numerical Methods",
        "Introduction to Cryptography", "Introduction to Combinatorics", "Software Engineering", 
        "Linear Programming Methods", "Theory and Applications of Pattern Recognition", 
        "Introduction to Programming Languages and Compilers", "Introduction to Operating Systems",
        "Introduction to Artificial Intelligence", "Introduction to Computer Architecture", 
        "Computer Graphics", "Database Management Systems: Design and Implementation",
        "Introduction to Human-Computer Interaction", "Introduction to Algorithms",
        "Undergraduate Elective Topics in Computing", "Introduction to Computer Networks", 
        "Machine Learning"
    ],
    "avg_gpa": [
        3.278, 2.9, 3.072, 3.097, 3.306, 3.197, 3.066, 3.249, 3.321, 3.352, 3.447, 2.978, 3.078, 3.297, 
        3.153, 3.263, 3.448, 3.063, 3.092, 3.255, 3.346, 3.086, 3.31, 3.422, 3.679, 3.549, 2.975, 3.55, 
        3.738, 2.968
    ],
    "total_grades": [
        12600, 10147, 9258, 9196, 8587, 7777, 7363, 7278, 6993, 6437, 5929, 5485, 4832, 4200, 3502, 
        3441, 2561, 2557, 2548, 2533, 2281, 2180, 2143, 2024, 1982, 1929, 1857, 1848, 1755, 1620
    ]
}

df = pd.DataFrame(data)
