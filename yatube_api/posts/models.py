from django.contrib.auth import get_user_model
from django.db import models

from .constants import STR_LENGTH, TITLE_MAX_LENGTH

User = get_user_model()


class Group(models.Model):
    """Тематическая группа публикаций."""

    title = models.CharField('Название', max_length=TITLE_MAX_LENGTH)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __str__(self):
        return self.title[:STR_LENGTH]


class Post(models.Model):
    """Публикация пользователя."""

    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    image = models.ImageField(
        'Картинка', upload_to='posts/', null=True, blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
    )

    class Meta:
        # Задаю порядок, чтобы пагинация отдавала стабильные страницы.
        ordering = ('pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'

    def __str__(self):
        return self.text[:STR_LENGTH]


class Comment(models.Model):
    """Комментарий к публикации."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    text = models.TextField('Текст')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text[:STR_LENGTH]


class Follow(models.Model):
    """Подписка пользователя на автора."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = (
            # Нельзя подписаться на одного автора дважды.
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_user_following',
            ),
            # И нельзя подписаться на самого себя даже в обход API.
            models.CheckConstraint(
                condition=~models.Q(user=models.F('following')),
                name='prevent_self_follow',
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
