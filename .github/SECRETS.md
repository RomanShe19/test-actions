# Настройка секретов для GitHub Actions

Для работы CI/CD pipeline необходимо настроить следующие секреты в вашем GitHub репозитории.

## Как добавить секреты:

1. Перейдите в Settings → Secrets and variables → Actions
2. Нажмите "New repository secret"
3. Добавьте каждый из секретов ниже

## Необходимые секреты:

### SSH_HOST
- **Описание**: IP-адрес или доменное имя вашего удаленного сервера
- **Пример**: `192.168.1.100` или `server.example.com`

### SSH_USERNAME
- **Описание**: Имя пользователя для SSH подключения
- **Пример**: `root` или `deploy`

### SSH_PRIVATE_KEY
- **Описание**: Приватный SSH ключ для подключения к серверу
- **Как получить**:
  ```bash
  # На вашем локальном компьютере или сервере CI/CD
  ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions
  
  # Скопируйте ПРИВАТНЫЙ ключ (содержимое файла ~/.ssh/github_actions)
  cat ~/.ssh/github_actions
  
  # Скопируйте ПУБЛИЧНЫЙ ключ на удаленный сервер
  ssh-copy-id -i ~/.ssh/github_actions.pub user@your-server
  ```
- **Важно**: Скопируйте весь ключ, включая строки `-----BEGIN OPENSSH PRIVATE KEY-----` и `-----END OPENSSH PRIVATE KEY-----`

### SSH_PORT
- **Описание**: Порт SSH на удаленном сервере
- **Пример**: `22` (по умолчанию) или другой порт, если вы его изменили
- **По умолчанию**: Если не указан, используется порт 22

## Автоматические секреты (не требуют настройки):

### GITHUB_TOKEN
- Автоматически предоставляется GitHub Actions
- Используется для публикации образов в GitHub Container Registry
- Не требует ручной настройки

## Подготовка удаленного сервера:

### 1. Установите Docker на сервере:
```bash
# Для Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER
```

### 2. Убедитесь, что порт 8000 открыт:
```bash
# Для UFW (Ubuntu)
sudo ufw allow 8000/tcp

# Для firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 3. Проверьте SSH доступ:
```bash
ssh -i ~/.ssh/github_actions user@your-server
```

## Проверка настройки:

После добавления всех секретов:
1. Сделайте коммит в ветку `main` или `master`
2. Перейдите в Actions → выберите workflow "Build and Deploy"
3. Проверьте логи выполнения

## Безопасность:

- ✅ Никогда не коммитьте приватные ключи в репозиторий
- ✅ Используйте отдельный SSH ключ только для GitHub Actions
- ✅ Ограничьте права пользователя SSH на сервере
- ✅ Регулярно обновляйте ключи
- ✅ Используйте сильные пароли и ключи

## Дополнительные переменные окружения (опционально):

Если вашему приложению нужны дополнительные переменные окружения, добавьте их в секреты и используйте в workflow:

```yaml
docker run -d \
  --name time-server \
  -p 8000:8000 \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  -e DEBUG=False \
  -e CUSTOM_VAR=${{ secrets.CUSTOM_VAR }} \
  ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
```

