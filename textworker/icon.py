from wx.lib.embeddedimage import PyEmbeddedImage

#----------------------------------------------------------------------
dev = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAABmJLR0QA/wD/AP+gvaeTAAAM'
    b'30lEQVR4nO2de3BU1R3Hv+fu3b13s0l2N9kN4VnyIC9AY219ofIGWyspaGfUznRaRxCFsUgg'
    b'bUVFnLZa2oDWtorwR63tHw4zpBbk0daKOiYCQkLIg7dAIORNXrubfd3TPzZEIAlkN+dsXO75'
    b'zJyZ7CY5v9/mfu7v/O7de7OAQCAQCAQCgUAgEAgEAoFAIBAIBIKbGRKNID99dOlEt8/1dn19'
    b'07T29k5Lj6cnKnFjAUIILBZz0G63tTgc9q01J8oLq6urfVGLzzvAooLHf3P86Olf9fR4xUYf'
    b'AjZbgttmT3zwv3t37I1GPK4bZf6cRW+ePnlmOaWUZ5ibDtkoa1Zr4px9Bz/6mHcsbgLMmVEw'
    b'59zZ8//RNI1XiJsas1lxt3b6nfX1B90840i8JnZ1u94RGz9yPB5v3PjRia/yjsNFgDvumJ3c'
    b'2tqexmNuPeH1+h/lHYOLAEk26w81Lchjal3h6nY7wbFKg+PkGZzm1RWUUjJhwlQrzxhcBDAQ'
    b'ycxjXj0SFzTHZAUQxAhCAJ0jBNA5QgCdIwTQOUIAnSOPZHBiMMLgnAQYTNEJGOhBoPkkoAX6'
    b'fUtKSIWUmDrkqQgogh310LqbWWYYdUZMAGKyIKHg9zDYxkc1brD1FDq3/xLw9/Q9FzdtKZTc'
    b'7wMkzPfGqIaeyhJ49v+VbZJRZMSWAFPmjKhvfAAwJGdASbun77HszISS92D4Gx8AiAT11och'
    b'2cYxzDC6jJgANBi1i176ofm9X3/t6wGGcb0C1bSrqkmsMWIC+E7uhf/CoejHPVsG/9kv+h5r'
    b'Hefh/vwtUF/4b7tTbxc8n/4RmquFZYpRZeSawKAf3TvXQjLbAWOUmkCfF1pPe7+nvbW74D26'
    b'B5IlGZCGuE8Eg9DcbQCN7WseRvQoAAA0zyXAM9JZAKBazHf0kSDOA+gcIYDOEQLonBHvAYaK'
    b'KecBKJNmAjKjhpFSBBuPwv3le4D/6ybEYBsP9bs/gRTvYBNnALRLdfAceBeaq5VbjKESEwLI'
    b'Y/NhuW8Z+3mdkwBQuMs2h54gBPHzXwrrlHBEODJBLMno/nAN3zhDICaWAIOD3yWGV85NjHH8'
    b'N34vsiMzKnFuREwIEKw7CHC6yth/dn/f19TnQqChhkuc68UdSWJiCQi0nUHnv4qgZE4HDAqj'
    b'WYMINNbCd/KTq57t3rMOyuSHIFmcjOIMELn9HLy1u7jNHw4xIQAABJuPw918nHsc6nOjp/x9'
    b'7nG+KcTEEiDghxBA5wgBdI4QQOcIAXSOEEDnCAF0jhBA54zYiaAVK5/GsmcXD/nn9+z6CMuf'
    b'Xs0xI30iKoDOGbEK8MbGt/HmG5uG/PPiP83xYcQEoJQiGBRbdaQRS4DOEQLoHCGAzhEC6Bwh'
    b'gM4RAugcIYDOEQLoHCGAzhEC6BwhgM4RAugcIYDOEQLoHCGAzhEC6BwhgM4RAugcIYDOEQLo'
    b'HCGAzhEC6BwhgM4RAugcIYDO4XJnUHx8+4QJEzQQaegfw2I2G5HiSGCaRzCo4Xx9/88HGC5j'
    b'U22QjWz3ndbWbnS7r/4UlUAAsKhInnoP2rduBZd/lMhFgNIvTqU0tzSBhnFDHyHAqhXfxqIF'
    b'6Uxz+WBHAOs3lkPT2N2GdsuUZGxcfx/izOz+fE3Nbjyz4hNcqHf1PScbZMiEJHa4IQF8BDDw'
    b'mNSaaH/C7XZNCPf3yvZdhN2mIDfbBoAyGTlZNjiSzSjd18DsBtPGJg8qDjdj9oyxMMqESZ6W'
    b'OBkz7huLz0ovoqvLDwCQJAkSIZu9fm8jAC4fTfKNEgAAyvY1hCTIsTPLJyfLBkcSBwkqWzB7'
    b'+jgYGS0HFosRM+4d0yeBLgUAgLL9DbDbTIwrgRWOZBWl+xoZS9CM2fePgdHIqBJY5JAEZQ1w'
    b'uYL6FAAAyvY3wm41ITfbCmYSTLosQRP7SnD/aLYSTBuDT0sb4HYF9CkA0CuBzYTcLBuLtACg'
    b'VwIFpfsZStDsQUVlK2ZPHw2jzGo5kHHr5GR8WdG6ufVStz4FAICy/U2w20zIyWJXCbIvVwLm'
    b'ErRh1v2pzBpDgODO21I2n7l4ovHiRT4CcDkRlJ7G7nieUqD4T9XYsbsOrAQAKBZ8bxwKl+VF'
    b'9Imxg1FZ3YbCNQfg8fiZ5ZnskLFp0xJ2SV4DFwGWL85GXo6V2XyaRvHa60ewY/c5gGrMxsIf'
    b'jMeq5WwlOFzVhpVrvoTH7WeQY6g83c4uvX5wEcCsEhSvuw35U9kdymkaxasbq1CynbEED47D'
    b'L57NgxTGWcsbcbiqDc89fwBuFwMJ/P0/6p4lfN4L0CgURcKGV9hKQCnwhz/XoGRHXegBo7Hg'
    b'gbEoWp7LVILKmnasfOEg3O7A8PLjDB8BKAWoBlUh2LDuVuRPYdfFhySoRckOtpVgwQOjUbQ8'
    b'h5MEEVYCPn3fVXB8NzDUxKiqhA2vcJDgL8dQ8uH5vjgsRkiCbMYSdGDli+VwewIR5sUXTgJo'
    b'uPJFhCS4JYYkyOIgQUVoOQg7Jz+zPAaCkwCX17Cvy1loOZiK/Cnsjg5CEhxHyY7zbJeD+ako'
    b'WjaJvQQvVYTZGF6uAAeZ5XEtHHuA/kNVCDa8PIW9BG+dQMmHFwaNG1FjOD8VRcsyGUvQiZVr'
    b'K3t7gpu5CcTgVqsKwYa1k5E/OZFZtJAEJ1Gy8wLbSjBvFIqeyeAgQdXQG0POcDsMvN6LUhWg'
    b'eG0eBwlOYdvOesYSpGD1M+nsJXi5Gi7PECTwx2oPcINhVgmK1+Ywl6D47dPYtqthSDkMdRTM'
    b'S8Hqp9OYS1C4tgauGx4d8IXreYAbDbNCUPxSNh8JdjYwrQQF85xYvZSxBLVdKHy5Fq5Bl4NY'
    b'FQDAUJuckASTkJ/H+A2kTV/1SsCuMSyY58Dqpd9iL8G6o3ANdsaQM5wqQDCsvcts4iTBO2dD'
    b'ywHLSjDXgdVLJzCWoBuFrxzrleDaJjAme4De3MPYu8wmguIXMzlIcA7bdjWxrQRzLkvALNVe'
    b'CY7D5Qn2xQmtpISiK4FbKeAigEFCgETQbJkVguIX0pGfF88sF0qB4s3nsG13U9j5XG8UzEnG'
    b'6qcYS3D0sgShxpBSinGpwQ58spfb8SCXK4KW/DjrYWjubKMMhPuHNcoEs6bZUFnrQkOzb8D5'
    b'I6HsUCfsVgNyM8xh5zTYyEk3w5FkROmhTmbLdWOLH4drujHzbhs0zYBbptD1pkfOd7KZvT9c'
    b'KkC8xdShUUPE66zZBBSvmYj8PAuznEKV4Dy27W6OOK8BzxPMtqPoqXGMK4ELhb8+CUoMoFTi'
    b'2glyESAYIH6zOW5Y66zZRFD8PAcJtlzAtj0tw8qt32njWXYULRnLVIIjx9x4/d02tLa42U06'
    b'AHyWgMeyZyuqcqdR8iAYiPRtUAqjAZh1txWVx1xoaGbXDZeVd8GeKCM3Q404t2tHdpoKh92I'
    b'0vIuJstBfIIF/qA58M+PT2+or/d3D3/GgeEiwGMPpU+VTepchx0IBgMIBCK/rc0oA9PvSEB5'
    b'jQdNrewk+KKiCynJRmSlqczmzE5XYUuUUVY+vO0VHx8He5INqqp2lJfXvQnAdcNfihAuAhw4'
    b'0ird853Mx1OTe2SLxQzZKMPv80HTNESyd5mMBLPuSkB5rRtNrWyukaMU+PxQF5xJMrImKhHl'
    b'NdDIzVBhTzSgrCL8baYoJiQlWxFnVhEXFwdFUSvq6+vfA9Az3Nc7GAyvh72KMQsL5v7jhSfp'
    b'jNGjjDAaJFBQeL0++H1+BINBRFIlPV6KVa9dQEUtu3WREKDwiRQsnMvuYhUA2P6/Dqzf0gjt'
    b'BgdwhBDIBgNMigkmoxEapdA0DSkpo9Dd3fXzqqqqLQC4NQK8BDBkZGQ9NDV39PvrlimmMU4Z'
    b'FKEXpmn0ikoQPh6vhlW/q0dFrYdZsoQAhT9LwcK57K5TAIDtH3dg/Zam60pACAndBCpJkIgE'
    b'jVIoigKn03l47969MwF0gOPFgVyWAAD00qXWttTUtJ7yo+T+2yfLxKJqoJT2jUgFMBoIZt0V'
    b'j8rjPWhoYXfJdFmFC/ZEA3LTFWZzZk9U4LTLKK1wDdoYEkL6hmSQYDarmDhxYnN1dfXirq6u'
    b'Y+B8ZSgvAQDAc+bsmSNWe2rgq4ak23PSFZOqUIAGEXpNkfUDAIVRBmbdGY/KY6wlcMNulZCb'
    b'boo4t/5HB6ZeCdwDSBDa+00mIxITE5GamopRTueJyiNVi+vq6vYB8DJ7cYPAawm4EikjI+Pu'
    b'mfdOWbH0R+q91gRfEtX8JkKHL3aPT8NvN7Wg5hS7vxMhwJOP2DF/GrvT0QDwUVk3Nm291G85'
    b'kGWZqmazJz7ecoYQ8sHu3f/eCOASAL53hPQSDQEAwARAzRoD0+6/pRlG2VRmp0zcbmDRc2fx'
    b'2UG2fdLG5x1YssjJdM6/b2vGU79tGehbQYQ2uBeAB9G4IUAgEAgEAoFAIBAIBAKBQCAQCAR6'
    b'4f+bexpEBJNxTQAAAABJRU5ErkJggg==')

#----------------------------------------------------------------------
stable = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAABmJLR0QA/wD/AP+gvaeTAAAG'
    b'AUlEQVR4nO3df2gXdRzH8dfd97vv7fZ13+99v/tOZ3PW3JZllAWpoUZGCyUNxQhEoiKI+YsI'
    b'oygSI8Ii+iNMIqt/iv6q/ghKZ6MsDcLSVAjmZE1xOsdsP77fze/u+2t31x/WTJT6zr7vu+77'
    b'fj/+2m7j8z645+7u+92xAUIIIYQQQgghhBBCCCGEKGeKG0OeXLfhJjM/vru///clqdRYOJvJ'
    b'ujLXDxRFQTisW7GYMZRIxD4/8dvx5zo7O/OuzacesHb1+h3dJ0+/lM3m5KAXwTCqTSMWWfnt'
    b'gT0H3JhHelCWt67ddbrnzBbHcSjHlJ1gRdCORiOtPx/d/z31LLIAWpetbj3b2/eNbdtUI8qa'
    b'rmvm8Fihtr//qEk5R6VaeDw9/oEc/OuXyeSqGmZG3qCeQxLAwoUP1AwPpxop1uYklyuso55B'
    b'EkDciK6xbYtiaVbG02YtCM/SIFy8iWhdVhzHUWbPvj1KOYMkgICi6hTrclRl6b48AwifkACY'
    b'kwCYkwCYkwCYkwCYC3o5XAlUIFDbAgRC7gycyGJisAewJ676klpdBzVSV/RSChxYo/2w04Ol'
    b'3EPXeRaAEgqjevVbCBgNrs61hk9h7KsXgUJ2clvVkg3Qbn0IUKb4uzHHRvbXL5A5/FFpd9JF'
    b'nl0CQs3LXD/4ABCoaYLWuHjy82BtM7R5K6d+8AFAUVE5/xGoxqwS7qG7PAvAsVx76OUqdiF3'
    b'+eN8FvgPzys4tn3F2cRvPAsg33MAhfPH3J/bewiF3p8mP7dH+2D++B6c/NR/7e7kLiLzwzuw'
    b'x4dKuYuu8u4m0Cog3f4KVD0GVLh0E5jPwc6mrtqc69qH3MkOqOEaQC3yZ8KyYJsjgOPvZx48'
    b'fRUAAHYmCWS83gsAju37O/rrIe8DMCcBMCcBMOf5PUCxQresgNZyPxAs0Q2j48C6cBLmL58A'
    b'hcs3IQGjAZULHoc6LVGaOddgJ88hc+Rj2OPDZDOK5YsAgvV3Inzv5tKvW9sCwIF56MNLGxQF'
    b'05Zvn9Jbwtcl0QwlXIP03pdp5xTBF5eAQILuEcO/r61UVNEf/D8FE82uzPk3vgjAOncUIHrK'
    b'uNB7ePJjJz+OiYETJHP+aa6XfHEJmBg5g7EvX4DWfB8Q0Eq0qoWJC13I9xy8Ymu641Votz0M'
    b'NVxbojnXmJw6i1zXPrL1p8IXAQCANdgNc7CbfI6TN5E9/in5nP8LX1wCBB0JgDkJgDkJgDkJ'
    b'gDkJgDkJgDkJgDnP3gh6dutGbH7m6aK/v2PffmzZ+DzhHvEkZwDmPDsD7Hx7N3btfL/o75e/'
    b'NEfDswAcx4FlyVH1mlwCmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMA'
    b'mJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMA'
    b'mJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmJMAmCMJ'
    b'IBgKZCnW5UfBhD6SppxAEoBhRIco1uWmqqoSPT09OcoZJAHMmFk7ZMSiFEuzUj+rjnwG2T3A'
    b'HfPnUi3NgqoqmDuviX4OyaIO0k0tjZgzZzbF8iwsvOcuGLHIReo5JAEojtqnKApWrXkQLTc3'
    b'Uowoa4uX3o0Fi+YDQB/1LJL/Gzg8duFYdWzaaChUEX3iqUdxorMbX7cfxMhwkmJc2WhsbMCK'
    b'VcswfXoCyeQoAHxHPVOhWnjHjjffrYkbm+LxKOJxA5Zl4fSpMzjfN4DU6EXYtk012ldCFUHE'
    b'4zHc2NiA+vo65HJ5jIykkEyOOqmh5KLtr20/Qjmf7D+HOk7F61CwHoDx17aZN8yAEYvANE1Y'
    b'lkU12lc0TYOu69B1/covKPiM+uADhK8Ctm3bel6x8RiAAtWMMtalaaE2NwaRvhXctqltLxR7'
    b'JYAByjnlRIHToeXzS9va2kbdmeeC9vb2SFDFBjNjrs1kzBbTzMTlEnCJpmmWrusDemXlIT0c'
    b'/ri1dfker/dJCCGEEEIIIYQQQgghhBDl4w/18Jk81Zot8QAAAABJRU5ErkJggg==')
